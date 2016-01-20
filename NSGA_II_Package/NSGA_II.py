#_*_ coding:utf-8 _*_
'''
Created on 2016年1月20日

@author: bush2582
@email : bush2582@163.com
'''
import sys, random
from sphinx.domains import Domain
import logging
class NSGA_II(object):
    '''
    classdocs
    '''
    

    def __init__(self, num_objectives, mutation_rate=0.1, crossover_rate=1.0):
        self.num_objectives = num_objectives #目标函数个数
        self.mutation_rate  = mutation_rate  #变异率
        self.crossover_rate = crossover_rate #交叉率
        
        self.Is_Dominance_Handle = self.Is_Dominance
        self.crowded_comparison_Handle = self.crowded_comparison
        self.Evolve_A_Generation_Handle = self.Evolve_A_Generation
        random.seed();
    
    def run(self, Init_Population, population_size, num_generations):
        '''
        function :基础非支配排序运算主流程
        para：1、P 初始种群  2、population_size 种群数量  3、num_generations 进化代数
        '''
        #评价适应度
        for e in Init_Population:
            e.evaluate_solution()
        #分层并计算拥挤度
        fronts = self.fast_nondominated_sort(Init_Population ) 
        for front in fronts.values():
            if len(front) == 0:
                break
            self.crowding_distance_assignment(front);
        #新种群
        New_Population = self.make_new_pop(Init_Population)
        Population = []
        for i in range(num_generations):
            Select_Pool =[]
            if i == 0 :
                Select_Pool.extend(Init_Population)
                Select_Pool.extend(New_Population)
            else :
                Select_Pool.extend(Population)
                Select_Pool.extend(New_Population)

                
            Population = self.Evolve_A_Generation(i,Select_Pool , population_size)
            New_Population = self.make_new_pop(Population)
            

        return Population 
    
    def Evolve_A_Generation(self,Generation,Population,population_size):
        print  "*******************Iteracao(%d)*******************" % Generation
             
        Ret_P = []
        
        fronts = self.fast_nondominated_sort(Population) #bush2582 注 . 计算出非支配排序层，每个层是一个list list中保存着各个个体
        
        del Population[:]#删除种群
        
        #添加分层后的种群到新的种群中
        for front in fronts.values():

            if len(front) == 0:
                break
            
            #计算各个层的种群的拥挤度
            self.crowding_distance_assignment(front);
            Ret_P.extend(front)
            
            #如果当前的种群数量>N 就跳出循环
            if len(Ret_P) >= population_size:
                break
        
        self.sort_crowding(Ret_P)

        
        if len(Ret_P) > population_size:
            del Ret_P[population_size:]
            
        return Ret_P
    
    def make_new_pop(self, P):
        '''
        function:选择，交叉，变异，生成新的种群 
        para:1、P 父种群
        '''
        Q = []
        
        while len(Q) != len(P):
            selected_solutions = [None, None]
            
            while selected_solutions[0] == selected_solutions[1]:
                for i in range(2):
                    s1 = random.choice(P)
                    s2 = s1
                    while s1 == s2:
                        s2 = random.choice(P)
                    
                    if self.crowded_comparison(s1, s2) > 0:
                        selected_solutions[i] = s1
                        
                    else:
                        selected_solutions[i] = s2
            
            if random.random() < self.crossover_rate:
                child_solution = selected_solutions[0].crossover(selected_solutions[1])
                
                if random.random() < self.mutation_rate:
                    child_solution.mutate()
                    
                child_solution.evaluate_solution()#计算子种群适应度
                
                Q.append(child_solution)
        
        return Q
    
            
    def fast_nondominated_sort(self, P):
        '''
        function :快速检测个体间的支配关系，并进行非支配分层
        para:1、P 种群
        '''
        fronts = {}
        
        S = {}
        n = {}
        for s in P:
            S[s] = []
            n[s] = 0
            
        fronts[1] = []
        
        for p in P:
            for q in P:
                if p == q:
                    continue
                
                if  self.Is_Dominance_Handle(p,q) == True:              #如果品p 支配 q
                    S[p].append(q)
                
                elif  self.Is_Dominance_Handle(p,q) == True:            #如果 q 支配 p
                    n[p] += 1
                    
            if n[p] == 0:#如果q和p无法比较支配关系的话，p就不会进入 S[]中
                p.rank = 1              #bush2582添加
                fronts[1].append(p)
        
        i = 1
        
        while len(fronts[i]) != 0:
            next_front = []
            
            for r in fronts[i]:
                for s in S[r]:
                    n[s] -= 1
                    if n[s] == 0:
                        s.rank = i + 1          #bush2582添加
                        next_front.append(s)
            
            i += 1
            fronts[i] = next_front
        

        return fronts    
    
    def crowding_distance_assignment(self, front):
        '''
        function  :对于每一个输入的前沿，进行计算拥挤度的操作
        para      :1、front 前沿 
        '''
        #对前沿每个个体的拥挤度赋0
        for p in front:
            p.distance = 0
            
        for obj_index in range(self.num_objectives):        #对于每个目标函数
            self.sort_objective(front, obj_index)           #基于这个目标函数对种群进行排序
            
            front[0].distance = float('inf')                #bush2582注 令边界的个体拥挤度无穷大
            front[len(front) - 1].distance = float('inf')
            
                
            Max_objectives = front[len(front)-1].objectives[obj_index]
            Min_objectives = front[0].objectives[obj_index]  
            
            if (Max_objectives-Min_objectives) == 0 :   #如果值一样。为了防止除0需要处理下
                Max_objectives = front[len(front)-1].objectives[obj_index]
                Min_objectives = 0

            #计算拥挤度
            for i in range(1, len(front) - 1):
                front[i].distance +=( (front[i + 1].objectives[obj_index] - front[i - 1].objectives[obj_index]) )/(Max_objectives-Min_objectives)

    def Is_Dominance(self,Fir_Individual,Sec_Individual):
        '''
        funtion    :非支配排序基础的比较支配关系的函数
        para       :1、Fir_Individual 被比较的第一个个体（要求其必须继承slution类）
                    2、Sec_Individual 被比较的第二个个体（要求其必须继承slution类）
        '''
        dominates = False
        
        for i in range(self.num_objectives):
            if Fir_Individual.objectives[i] > Sec_Individual.objectives[i]:
                    return False
                     
            elif Fir_Individual.objectives[i] < Sec_Individual.objectives[i]:
                    dominates = True
        return dominates            
    
    def crowded_comparison(self,s1, s2):
        '''
        function:比较两个个体之间的优先级
        para:1、s1 2、s2 s1 s2 为两个要比较的个体
        '''
        
        if s1.rank < s2.rank:
            return 1
            
        elif s1.rank > s2.rank:
            return -1
            
        elif s1.distance > s2.distance:
            return 1
            
        elif s1.distance < s2.distance:
            return -1
            
        else:
            return 0
        
    def sort_objective(self, P, obj_idx):
        '''
                        使用冒泡排序，根据目标函数进行排序
        '''
        for i in range(len(P) - 1, -1, -1):
            for j in range(1, i + 1):
                s1 = P[j - 1]
                s2 = P[j]
                
                if s1.objectives[obj_idx] > s2.objectives[obj_idx]:
                    P[j - 1] = s2
                    P[j] = s1
        
    def sort_crowding(self, P):
        for i in range(len(P) - 1, -1, -1):
            for j in range(1, i + 1):
                s1 = P[j - 1]
                s2 = P[j]
                
                if self.crowded_comparison_Handle(s1, s2) < 0:
                    P[j - 1] = s2
                    P[j] = s1


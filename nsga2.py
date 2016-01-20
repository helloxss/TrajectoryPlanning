
# _*_ coding:utf-8 _*_
'''
Created on 07/01/2011

@author: 04610922479
'''

import sys, random
from sphinx.domains import Domain
import logging
from Decorator_CheckDominace import Decorator_CheckDominace
class Solution:
    '''
    Abstract solution. To be implemented.
            虚基类。其接口需要被实现
    '''
    
    def __init__(self,num_objectives,num_const):
        '''
        methonName:__init__
        function:初始化
        para:1、num_objectives 目标函数个数
             2、num_const 约束个数
        '''
        self.num_objectives = num_objectives
        self.num_const      = num_const


        
        self.const_LimitValue   = [0]*num_const   #各个约束的极限值
        self.const_Value        = [0]*num_const   #各个约束的当前值
        self.objectives         = [0]*num_objectives #目标函数值列表
        self.attributes         = []                #属性列表
        
        self.rank = sys.maxint  #rank等级
        self.distance = 0.0
    
    
       
    def evaluate_solution(self):
        '''
                        求取适应度 接口
        '''
        raise NotImplementedError("Solution class have to be implemented.")
    
    def crossover(self, other):
        '''
                        交叉接口
        '''
        raise NotImplementedError("Solution class have to be implemented.")
    
    def mutate(self):
        '''
                        变异操作接口
        '''
        raise NotImplementedError("Solution class have to be implemented.")
    
   
    
    def __rshift__(self, other):
        '''
        True if this solution dominates the other (">>" operator).
        '''
        dominates = False
        for i in range(len(self.objectives)):
            
            if  self.Infeasible_Degree  <   self.Infeasible_Degree_Threshold        and \
                other.Infeasible_Degree >   other.Infeasible_Degree_Threshold:#当前解可行，其他解不可行
                return True 
            
            elif    other.Infeasible_Degree < other.Infeasible_Degree_Threshold     and \
                    self.Infeasible_Degree  > self.Infeasible_Degree_Threshold:#当前解不可行，其他解可行
                return False 
            elif    other.Infeasible_Degree > other.Infeasible_Degree_Threshold     and \
                    self.Infeasible_Degree  > self.Infeasible_Degree_Threshold      and \
                    self.Infeasible_Degree  >= other.Infeasible_Degree: #都不可行，是但是可行度大于其他解
                return False
            
            elif    other.Infeasible_Degree > other.Infeasible_Degree_Threshold     and \
                    self.Infeasible_Degree  > self.Infeasible_Degree_Threshold      and \
                    self.Infeasible_Degree  <= other.Infeasible_Degree: #都不可行，是但是可行度小于其他解
                return True
            
            elif    self.Infeasible_Degree  < self.Infeasible_Degree_Threshold      and \
                    other.Infeasible_Degree < other.Infeasible_Degree_Threshold:  #如果通过了约束
                
                if self.objectives[i] > other.objectives[i]:
                    return False
                     
                elif self.objectives[i] < other.objectives[i]:
                    dominates = True
                
        
        if  dominates == False:
            
            Dist = (self.R_Dist-other.R_Dist)/(self.MaxR_Dist-other.MinR_Dist)
            if Dist < self.R_Dominance_Threshol:
                return True
         
        return dominates
        
    def __lshift__(self, other):
        '''
        True if this solution is dominated by the other ("<<" operator).
        '''
        return other >> self


def crowded_comparison(s1, s2):
    '''
    Compare the two solutions based on crowded comparison.
    '''
    if s1.Infeasible_Degree > s2.Infeasible_Degree: #S1不可行阈值比S2来得大 ，就证明 S1不是好解
        return -1
        
    elif s1.Infeasible_Degree < s2.Infeasible_Degree:
        return 1
    
    elif s1.rank < s2.rank:
        return 1
        
    elif s1.rank > s2.rank:
        return -1
        
    elif s1.distance > s2.distance:
        return 1
        
    elif s1.distance < s2.distance:
        return -1
        
    else:
        return 0


class NSGAII:
    '''
    Implementation of NSGA-II algorithm.
    '''
    current_evaluated_objective = 0
    Decorator_CheckDominace = Decorator_CheckDominace()

    def __init__(self, num_objectives, mutation_rate=0.1, crossover_rate=1.0):
        '''
        Constructor. Parameters: number of objectives, mutation rate (default value 10%) and crossover rate (default value 100%). 
        '''
        self.num_objectives = num_objectives
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        
        self.Infeasible_Degree_Threshold = 0.0
        random.seed();
        
    def run(self, P, population_size, num_generations,g_Point):
        '''
        Run NSGA-II. 
        '''
        
        for s in P:
            s.evaluate_solution()
        
        Q = []
        
        for i in range(num_generations):
            print "Iteracao ", i
             
            R = []
            R.extend(P)
            R.extend(Q)
            
            #计算R支配的值
            Max_Objectives_Values = [-float('inf')]*len(R[0].objectives)
            Min_Objectives_Values = [ float('inf')]*len(R[0].objectives)
            
            
            for Individual in R:
                for i in range( len(Individual.objectives) ):
                    if Max_Objectives_Values[i] < Individual.objectives[i]:
                        Max_Objectives_Values[i] = Individual.objectives[i]
                        
                    if Min_Objectives_Values[i]> Individual.objectives[i]:
            
                        Min_Objectives_Values[i] = Individual.objectives[i]
 
            
            self.MaxR_Dist = (-float('inf'))
            self.MinR_Dist = float('inf')
            for Individual in R:
                Individual.Cal_R_Dominance_Value(g_Point,Max_Objectives_Values,Min_Objectives_Values)
                if  self.MaxR_Dist < Individual.R_Dist:
                    self.MaxR_Dist = Individual.R_Dist
                
                if  self.MinR_Dist > Individual.R_Dist:
                    self.MinR_Dist = Individual.R_Dist
                
            self.R_Dominance_Threshol = 1.0- (i*1.0)/num_generations
            

            #计算不可行度阈值
            for Individual in R:
                self.Infeasible_Degree_Threshold += Individual.Infeasible_Degree
            self.Infeasible_Degree_Threshold = (1.0/(i+1))*self.Infeasible_Degree_Threshold/(2*population_size)
            
            #填充计算需要的各个数据
            for Individual in R:
                Individual.Infeasible_Degree_Threshold = self.Infeasible_Degree_Threshold
                Individual.MinR_Dist =  self.MinR_Dist
                Individual.MaxR_Dist =  self.MaxR_Dist
                Individual.R_Dominance_Threshol = self.R_Dominance_Threshol
                
            
            
            
            
            
            fronts = self.fast_nondominated_sort(R) #bush2582 注 . 计算出非支配排序层，每个层是一个list list中保存着各个个体
            
            del P[:]#删除种群
            
            #添加分层后的种群到新的种群中
            for front in fronts.values():

                if len(front) == 0:
                    break
                
                #计算各个层的种群的拥挤度
                self.crowding_distance_assignment(front);
                P.extend(front)
                
                #如果当前的种群数量>N 就跳出循环
                if len(P) >= population_size:
                    break
            
            self.sort_crowding(P)

            
            if len(P) > population_size:
                del P[population_size:]
                
            Q = self.make_new_pop(P)
            
    def sort_ranking(self, P):
        for i in range(len(P) - 1, -1, -1):
            for j in range(1, i + 1):
                s1 = P[j - 1]
                s2 = P[j]
                
                if s1.rank > s2.rank:
                    P[j - 1] = s2
                    P[j] = s1
                    
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
                
                if crowded_comparison(s1, s2) < 0:
                    P[j - 1] = s2
                    P[j] = s1
                
    def make_new_pop(self, P):
        '''
        Make new population Q, offspring of P. 
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
                    
                    if crowded_comparison(s1, s2) > 0:
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
        Discover Pareto fronts in P, based on non-domination criterion. 
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
                
#                 if p >> q:              #如果品p 支配 q
#                     S[p].append(q)
#                 
#                 elif p << q:            #如果 q 支配 p
#                     n[p] += 1
                    
                if self.Is_Dominance(p,q) == True:              #如果品p 支配 q
                    S[p].append(q)
                
                elif self.Is_Dominance(p,q) == True:            #如果 q 支配 p
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

 


    
    @Decorator_CheckDominace.Is_Violate_Constraint
    @Decorator_CheckDominace.Is_R_Dominace
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
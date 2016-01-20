# _*_ coding:utf-8 _*_
'''
Created on 2016年1月20日

@author: bush2582
@email : bush2582@163.com
'''

class Decorator_OtherDefine_NSGAII(object):
    '''
    function:主要用来完成对于非支配排序基础算法以外的非支配排序进行处理。例如R支配，基于约束的支配
    '''
    

    def __init__(self):
        pass
    
    def Is_Violate_Constraint(self,func):
        '''
        function:装饰器，用于检测不可行度是否大于阈值
        '''
        def wrapper(*args, **kw):
            Infeasible_Degree_Threshold = args[0].Infeasible_Degree_Threshold
            Fir_Individual_Infeasible_Degree = args[1].Infeasible_Degree
            Sec_Individual_Infeasible_Degree = args[2].Infeasible_Degree
            
            if  Fir_Individual_Infeasible_Degree  <   Infeasible_Degree_Threshold       and \
                Sec_Individual_Infeasible_Degree  >   Infeasible_Degree_Threshold:#当前解可行，其他解不可行
                return True 
        
            elif    Sec_Individual_Infeasible_Degree < Infeasible_Degree_Threshold      and \
                    Fir_Individual_Infeasible_Degree > Infeasible_Degree_Threshold:#当前解不可行，其他解可行
                return False 
            elif    Sec_Individual_Infeasible_Degree > Infeasible_Degree_Threshold      and \
                    Fir_Individual_Infeasible_Degree > Infeasible_Degree_Threshold      and \
                    Fir_Individual_Infeasible_Degree >= Sec_Individual_Infeasible_Degree: #都不可行，是但是可行度大于其他解
                return False
            
            elif    Sec_Individual_Infeasible_Degree > Infeasible_Degree_Threshold      and \
                    Fir_Individual_Infeasible_Degree > Infeasible_Degree_Threshold      and \
                    Fir_Individual_Infeasible_Degree <= Sec_Individual_Infeasible_Degree: #都不可行，是但是可行度小于其他解
                return True
            
            func(*args, **kw)
        return wrapper   
    
    def Is_R_Dominace(self,func):  
        '''
        function:装饰器，用于检测R支配
        '''
        def wrapper(*args, **kw):
            if func(*args, **kw) == False: #如果检测过后发现并没有支配关系，就做R支配检测
                MaxR_Dist = args[0].MaxR_Dist
                MinR_Dist = args[0].MinR_Dist
                Fir_Individual_R_Dist = args[1].R_Dist
                Sec_Individual_R_Dist = args[2].R_Dist
                
                Dist = (Fir_Individual_R_Dist-Sec_Individual_R_Dist)/(MaxR_Dist-MinR_Dist)
                if Dist < args[0].R_Dominance_Threshol:
                    return True
                else:
                    return False
        return wrapper   
    
    def Crowded_comparison_Constraint(self,func):
        '''
        function:装饰器，用于在约束条件下比较个体登记
        '''
        def wrapper(*args, **kw):
            if args[1].Infeasible_Degree > args[2].Infeasible_Degree: #S1不可行阈值比S2来得大 ，就证明 S1不是好解
                return -1
         
            elif args[1].Infeasible_Degree < args[2].Infeasible_Degree:
                return 1
            func(*args, **kw)
        return wrapper   
    
    def Cal_Infeasible_Degree_Threshold(self,func):
        '''
        function:装饰器，用于在约束条件下计算不可行度阈值 装饰函数： Evolve_A_Generation(self, Generation, Population, population_size)
        '''
        def wrapper(*args, **kw):
            for Individual in args[2]:
                args[0].Infeasible_Degree_Threshold += Individual.Infeasible_Degree
            args[0].Infeasible_Degree_Threshold = (1.0/(args[1]+1))*args[0].Infeasible_Degree_Threshold/(2*args[3])
            
            return func(*args, **kw)
        return wrapper 
    
    def Cal_R_Dominance_Threshol(self,func):
        '''
        function:装饰器，用于在R支配下计算参数 。 装饰函数： Evolve_A_Generation(self, Generation, Population, population_size)
        '''
        def wrapper(*args, **kw):
            #计算R支配的值
            Max_Objectives_Values = [-float('inf')]* args[0].num_objectives
            Min_Objectives_Values = [ float('inf')]* args[0].num_objectives
            
            
            for Individual in args[2]:
                for i in range( len(Individual.objectives) ):
                    if Max_Objectives_Values[i] < Individual.objectives[i]:
                        Max_Objectives_Values[i] = Individual.objectives[i]
                        
                    if Min_Objectives_Values[i]> Individual.objectives[i]:
            
                        Min_Objectives_Values[i] = Individual.objectives[i]
 
            
            args[0].MaxR_Dist = (-float('inf'))
            args[0].MinR_Dist = float('inf')
            for Individual in args[2]:
                Individual.Cal_R_Dominance_Value(args[0].TargetPoint,Max_Objectives_Values,Min_Objectives_Values)
                if  args[0].MaxR_Dist < Individual.R_Dist:
                    args[0].MaxR_Dist = Individual.R_Dist
                
                if  args[0].MinR_Dist > Individual.R_Dist:
                    args[0].MinR_Dist = Individual.R_Dist
                
            args[0].R_Dominance_Threshol = 1.0- (i*1.0)/args[0].Num_generations
            
            return func(*args, **kw)
        return wrapper 
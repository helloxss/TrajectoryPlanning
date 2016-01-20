# _*_ coding:utf-8 _*_
'''
Created on 2016年1月20日

@author: bush2582
@email : bush2582@163.com
'''

class Decorator_CheckDominace(object):
    '''
    function:主要用来完成对于非支配排序基础算法以外的支配定义的处理。例如R支配，基于约束的支配
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
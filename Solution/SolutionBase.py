#_*_ coding:utf-8 _*_
'''
Created on 2016年1月21日

@author: bush2582
@email : bush2582@163.com
'''

class Solution:
    '''
            虚基类。其接口需要被实现
    '''
    
    def __init__(self,num_objectives,num_const):
        '''
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
        
        self.rank = -1
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
    
#_*_ coding:utf-8 _*_
'''
Created on 2016年1月21日

@author: bush2582
@email : bush2582@163.com
'''

import numpy as np
import math
class TOPSIS(object):
    '''
    TOPSIS算法实现类
    '''


    def __init__(self, Ret_Population,W_Matrix):
        '''
        function : 初始化，并完成加权判断矩阵
        para：1、Ret_Population 进化的结果种群  2、权重对角矩阵
        '''
        self.Population = Ret_Population
        self.PopulationSize = len(self.Population) 
        self.ObjectNums = len(Ret_Population[0].objectives)
        self.V_Matrix   = []    #判断矩阵 V
        self.Z_Matrix   = []    #加权判断矩阵
        self.W_Matrix   = []  #权重对角矩阵
        
        self.Ret_Population_objectives_SumList = [0]*self.ObjectNums # 归一化需要的list
        
        for Individual in self.Population:
            self.V_Matrix.append(Individual.objectives[:])
            
            for i in range( len(Individual.objectives) ):
                self.Ret_Population_objectives_SumList[i] += (Individual.objectives[i])*(Individual.objectives[i])
        
        for i in range( self.ObjectNums ):
            self.Ret_Population_objectives_SumList[i] = math.sqrt(self.Ret_Population_objectives_SumList[i])
            #建立权重对角阵
            Tmp = [0]*self.ObjectNums
            Tmp[i] = W_Matrix[i]
            self.W_Matrix.append(Tmp)
            
        #归一化处理
        for i in range(self.PopulationSize ):
            for j in range (len( self.Ret_Population_objectives_SumList ) ):
                self.V_Matrix[i][j] = self.V_Matrix[i][j]  / self.Ret_Population_objectives_SumList[j]
        
        
            
        #获得加权判断矩阵
        self.V_Matrix = np.array(self.V_Matrix)  
        self.W_Matrix = np.array(self.W_Matrix)  
         
        self.Z_Matrix = np.dot(self.V_Matrix,self.W_Matrix)

    def __GetBestTarget_And_WorstTarget(self):
        '''
        function :获得最好和最劣的解
        '''
        self.BestTargetList  = [-float('inf')]*self.ObjectNums
        self.WorstTargetList = [ float('inf')  ]*self.ObjectNums
        
        for i in range( self.PopulationSize ): 
            for j in range ( self.ObjectNums ):
                if self.Z_Matrix[i][j] > self.BestTargetList[j]:
                    self.BestTargetList[j] = self.Z_Matrix[i][j]
                
                if self.Z_Matrix[i][j] < self.WorstTargetList[j]:
                    self.WorstTargetList[j] = self.Z_Matrix[i][j]
        
       
    def __CalDist(self):
        '''
        function :计算各目标值与理想值之间的欧氏距离
        '''
        self.BestTarget_Dist  = [0]*self.PopulationSize
        self.WorstTarget_Dist = [0]*self.PopulationSize
        
        for i in range( self.PopulationSize ):
            for j in range(self.ObjectNums):
                self.BestTarget_Dist[i]+= pow( (self.Z_Matrix[i][j]-self.BestTargetList[j]),2 )
                self.WorstTarget_Dist[i]+= pow( (self.Z_Matrix[i][j]-self.WorstTargetList[j]),2 )
            self.BestTarget_Dist[i] = math.sqrt(self.BestTarget_Dist[i])
            self.WorstTarget_Dist[i] = math.sqrt(self.WorstTarget_Dist[i])
            
    def __CalTarget_Closeness_Degree(self):
        '''
        function :计算各个目标的相对贴近度
        '''
        self.Target_Closeness_Degree = [0]* self.PopulationSize
        
        for i in range( self.PopulationSize ) :
            self.Target_Closeness_Degree[i] = self.BestTarget_Dist[i]/(self.BestTarget_Dist[i]+self.WorstTarget_Dist[i])

    def GetMax_Satisfaction_Target(self):
        '''
        function :获得最满意解
        '''
        self.__GetBestTarget_And_WorstTarget()
        self.__CalDist()
        self.__CalTarget_Closeness_Degree()
        
        Max_Satisfaction_Target = None
        Max_Target_Closeness_Degree = ( -( float('inf') ) )
        for i in range( self.PopulationSize ) :
            if Max_Target_Closeness_Degree < self.Target_Closeness_Degree[i]:
                Max_Target_Closeness_Degree = self.Target_Closeness_Degree[i]
                Max_Satisfaction_Target = self.Population[i]

        return Max_Satisfaction_Target
        
        
        
        
        
        
        
        
        
        
        
    
    
    
    
    
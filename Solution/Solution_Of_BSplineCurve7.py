#_*_ coding:utf-8 _*_
'''
Created on 2016年1月21日

@author: bush2582
@email : bush2582@163.com
'''
from SolutionBase import Solution
import random, math
from Solution.SolutionBase import Solution
from BSplineCurve_Package.BSplineCurve import BSplineCurve
class Solution_Of_BSplineCurve7(Solution):
    '''
            轨迹规划个体类
    '''


    def __init__(self,Const_LimitValueList,PointList,Attributes):
        '''
        function：初始化
        para1、Const_LimitValueList:约束极限值
            2、AttributesList：属性变量，即时间间隔
            3、PointList：要插值的轨迹点
        '''
        
        Solution.__init__(self, 3, 3 )
        
        self.const_LimitValue = Const_LimitValueList
        self.attributes = Attributes             #属性，即遗传的编码。在这个环境中是 时间间隔
        self.pointList  = PointList             #轨迹规划的点
        self.Infeasible_Degree = 0              #不可行度
        self.R_Dist = 0 
    
    def SetPointList(self,PointList):
        '''
        function:重置PointList
        para：1、PointList 新点列表 
        '''
        self.pointList  = PointList
        
    def Cal_R_Dominance_Value(self,g_Point,Max_Objectives_Values,Min_Objectives_Values):
        '''
        function:计算R支配的阈值
        para：1、g_Point 参考点  2、Max_Objectives_Values 各个目标函数值的最大值的列表 3、Min_Objectives_Values 各个目标函数值的最小值的列表
        '''
        for i in range(len(self.objectives)):
            Tmp = (self.objectives[i]-g_Point[i])/(Max_Objectives_Values[i]-Min_Objectives_Values[i])
            Tmp = Tmp*Tmp
            self.R_Dist +=  Tmp
        self.R_Dist = math.sqrt(self.R_Dist)    
        
    def evaluate_Infeasible_Degree(self):
        '''
        function：计算 当前这个个体的不可行度
        '''
        
        #获得要限定的约束的约束值
        self.const_Value[0] = self.BSplineCurve.GetMaxD_Control("V")#速度约束
        self.const_Value[1] = self.BSplineCurve.GetMaxD_Control("A")#加速度约束
        self.const_Value[2] = self.BSplineCurve.GetMaxD_Control("J")#加加速度约束
 
        #计算当前这个个体的不可行度
        for i in range(self.num_const):
            if ( self.const_LimitValue[i] -self.const_Value[i] ) > 0 :
                self.Infeasible_Degree += 0
            else:
                self.Infeasible_Degree += ( self.const_LimitValue[i] -self.const_Value[i] )*( self.const_LimitValue[i] -self.const_Value[i] )
        
        
    def evaluate_solution(self):
        '''
        function:计算 当前这个个体对于各个函数的适应度
        '''
        #将时间间隔转化为时间点
        self.TList= [0]*len(self.pointList)
        for i in range(1,len(self.pointList)):
            self.TList[i] =self.TList[i-1]+ self.attributes[i]
            
        self.BSplineCurve =  BSplineCurve(self.TList,7,self.pointList)
        self.BSplineCurve.CalBSplineCurve()
        
        self.objectives[0] = self.BSplineCurve.GetTall()            #时间最小
        self.objectives[1] = self.BSplineCurve.GetE_J_Level("J")    #最平滑
        self.objectives[2] = self.BSplineCurve.GetE_J_Level("E")    #能量最小
        
        self.evaluate_Infeasible_Degree()#计算不可行度
       
    def crossover(self, other):
        '''
        function:交叉
        para:1、other 另一个个体
        '''
        child_solution = Solution_Of_BSplineCurve7(self.const_LimitValue,self.pointList,self.attributes)
        
        for i in range( len(self.attributes) ):
            child_solution.attributes[i] = math.sqrt(self.attributes[i] * other.attributes[i])
        
        return child_solution
    
    def mutate(self):
        '''
        function:变异
        '''
        mutate_value = 0
        while mutate_value == 0.0: #保证不会出现0值
            mutate_value = (random.random()*2)
        self.attributes[random.randint(0, len(self.attributes)-1)] = mutate_value
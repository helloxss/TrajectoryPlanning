#_*_ coding:utf-8 _*_
'''
Created on 2016年1月21日

@author: bush2582
@email : bush2582@163.com
'''
from Init_TPopluation import Init_TPopluation
from NSGA_II_Package.NSGA_II import NSGA_II
from NSGA_II_Package.NSGA_II_With_Constraint_And_R_Dominance import NSGA_II_With_Constraint_And_R_Dominance
from NSGA_II_Package.NSGA_II_With_Constraint import NSGA_II_With_Constraint
from Solution.Solution_Of_BSplineCurve7 import Solution_Of_BSplineCurve7
from BSplineCurve_Package.BSplineCurve import BSplineCurve
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from TOPSIS import TOPSIS
class TrajectPlanning(object):
    '''
            轨迹规划类
    '''
    def __init__(self,Point_Matrix,ConstList,W_Matrix):
        '''
        function:初始化
        para:1、Point_Matrix 
        '''
        self.Point_Matrix = Point_Matrix    #轨迹点列表
        self.Crossover_rate = 0.7   #交叉率
        self.Mutation_rate  = 0.2   #变异率
        self.ObjectNums = 3         #目标函数个数
        self.PopulationNums  = 11  #种群数量
        self.Num_generations = 10   #进化代数
        self.ConstList = ConstList  #约束的列表
        self.Point_List_Len = len(Point_Matrix[0]) #插值点列 长度
        self.TargetPoint = []  #R支配目标点
        self.RetPoint = []     #结果集
        self.BSplineCurve_Population = [] #种群
        self.RetBSplineCurve_Population = [] #每次进化出来的种群
        self.Plt = []
        self.TOPSIS = None          #TOPSIS算法类
        self.W_Matrix = W_Matrix    #权重集
        
        
        self.NSGA_II_With_Constraint = NSGA_II_With_Constraint(self.ObjectNums,self.Mutation_rate,self.Crossover_rate)
        self.NSGA_II_With_Constraint_And_R_Dominance = None
        
        
    
    def __Init_BSplineCurve_Population(self,Point_List_Len):
        '''
        function:初始化种群
        para：1、Point_List_Len 插值点列 长度
        '''
        self.BSplineCurve_Population = []   #删除原有的种群  
        mInit_TPopluation = Init_TPopluation(Point_List_Len,self.PopulationNums) #随机时间间隔初始化
        TList = mInit_TPopluation.T_Population()
        
        for i in range(self.PopulationNums):
            self.BSplineCurve_Population.append( Solution_Of_BSplineCurve7( self.ConstList, self.Point_Matrix[0],TList[i]) )
    
    def GetFirstRet(self):
        '''
        function:对不采用R支配的插值进行 基于约束的非支配排序
        '''
        self.__Init_BSplineCurve_Population(self.Point_List_Len)
        P_Ret = self.NSGA_II_With_Constraint.run(self.BSplineCurve_Population, self.PopulationNums,self.Num_generations)  

        
        self.TOPSIS = TOPSIS(P_Ret,self.W_Matrix)     
        self.RetPoint.append(self.TOPSIS.GetMax_Satisfaction_Target())
        self.RetBSplineCurve_Population.append(P_Ret[:])

        for e in self.RetPoint[0].objectives:
            self.TargetPoint.append(e)
        

        self.Plt.append( self.DrawFig(P_Ret,self.RetPoint[0],"%d_BSplineCurve" % 0) )
        
        print "时间:"+str(self.TargetPoint[0])+", 平滑:"+str(self.TargetPoint[1])+", 能量:"+str(self.TargetPoint[2])+"\n"
    def GetOtherRet(self):
        '''
        function:采用R支配求解剩余的轨迹
        '''
        for i in range(1,len( Point_Matrix )):
            self.NSGA_II_With_Constraint_And_R_Dominance= NSGA_II_With_Constraint_And_R_Dominance(
                                                        self.ObjectNums,
                                                        self.Mutation_rate,
                                                        self.Crossover_rate,
                                                        TargetPoint=self.TargetPoint[:] )
            
            self.__Init_BSplineCurve_Population(self.Point_List_Len)
            P_Ret = self.NSGA_II_With_Constraint_And_R_Dominance.run(self.BSplineCurve_Population, self.PopulationNums,self.Num_generations)
           
            self.TOPSIS = TOPSIS(P_Ret,self.W_Matrix)  
            self.RetPoint.append(self.TOPSIS.GetMax_Satisfaction_Target())  
            self.RetBSplineCurve_Population.append(P_Ret[:])
            
            for j in range(len(self.TargetPoint)):
                if self.RetPoint[i].objectives[j] < self.TargetPoint[j]:
                    self.TargetPoint[j] = self.RetPoint[i].objectives[j] 
                    

            self.Plt.append( self.DrawFig(P_Ret,self.RetPoint[i],"%d_BSplineCurve" % i ))       
            print "时间:"+str(self.RetPoint[i].objectives[0])+", 平滑:"+str(self.RetPoint[i].objectives[1])+", 能量:"+str(self.RetPoint[i].objectives[2])+"\n"
    
    
            
    def DrawFig(self,P,RetPoint,Title):
        
        
        ListX= []
        ListY= []
        ListZ= []
        for e in P:
            ListX.append(e.objectives[0]) 
            ListY.append(e.objectives[1]) 
            ListZ.append(e.objectives[2]) 
            
        DrawT_List = np.linspace(0, 1, 300)
        NewList=[]
        for t in DrawT_List:
            NewList.append(RetPoint.objectives[0]*t)
        plt.figure(figsize=(12,10))    
        p1 = plt.subplot(211)     
        
         
        p1.plot(RetPoint.TList,RetPoint.pointList,"b*",label="org_point",linewidth=5)
        p1.plot(NewList,RetPoint.BSplineCurve.GetT_PList(DrawT_List),"b-",label="point",color="red",linewidth=2)
        p1.plot(NewList,RetPoint.BSplineCurve.GetT_VList(DrawT_List),"b-",label="V",color="green",linewidth=2)
        p1.plot(NewList,RetPoint.BSplineCurve.GetT_AList(DrawT_List),"b-",label="A",color="black",linewidth=2)
        p1.plot(NewList,RetPoint.BSplineCurve.GetT_JList(DrawT_List),"b-",label="J",color="blue",linewidth=2)
        
        p1.set_title(Title,fontsize=18)
        p1.set_xlabel("Time(s)")
        p1.set_ylabel("deg")
        p1.set_ylim(-200,200)
        p1.legend()
        
        
        ax = plt.subplot(212,projection='3d')

        ax.scatter(ListX, ListY, ListZ)
        ax.set_xlabel('Time')
        ax.set_ylabel('J')
        ax.set_zlabel('E')
    
        return plt
       
if __name__ == '__main__':
    P_List = [43.35,
              43.33,
              50.04,
              62.67,
              78.04,
              94.40,
              104.13,
              111.91]
    P_List1 = [43.35,
              43.33,
              50.04,
              62.67,
              78.04,
              89.40,
              97.13,
              100.91]
    P_List2 = [43.35,
              43.33,
              50.04,
              62.67,
              86.04,
              99.40,
              104.13,
              120.91]
    Point_Matrix = [P_List,P_List1,P_List2]
    mTrajectPlanning = TrajectPlanning(Point_Matrix,[110,80,80],[0.5,0.3,0.2])
    mTrajectPlanning.GetFirstRet()
    mTrajectPlanning.GetOtherRet()
    for e in mTrajectPlanning.Plt:
        e.show()
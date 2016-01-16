# _*_ coding:utf-8 _*_
'''
Created on 2016年1月12日

@author: Administrator
'''
import random, math
from nsga2 import Solution
from nsga2 import NSGAII
from BSplineCurve import BSplineCurve
from Init_TPopluation import Init_TPopluation
class BSplineCurve7(Solution):
    '''
    7次B样条轨迹规划
    '''


    def __init__(self,Const_LimitValueList,PointList,Attributes):
        '''
        Const_LimitValueList:约束极限值
        AttributesList：属性变量
        PointList：要插值的轨迹点
        
        '''
        
        Solution.__init__(self, 3, 3 )
        
        self.const_LimitValue = Const_LimitValueList
        

        self.attributes =Attributes

       

        
        self.pointList  = PointList
        self.Infeasible_Degree = 0.0
        self.Infeasible_Degree_Threshold = 0.0
        
        
        
        
    
    def evaluate_Infeasible_Degree(self):
        '''
                        计算 当前这个个体的不可行度
        '''
        
        self.const_Value[0] = self.BSplineCurve.GetMaxD_Control("V")#速度约束
        self.const_Value[1] = self.BSplineCurve.GetMaxD_Control("A")#加速度约束
        self.const_Value[2] = self.BSplineCurve.GetMaxD_Control("J")#加加速度约束

        
        for i in range(self.num_const):
            if ( self.const_LimitValue[i] -self.const_Value[i] ) > 0 :
                self.Infeasible_Degree += 0
            else:
                self.Infeasible_Degree += ( self.const_LimitValue[i] -self.const_Value[i] )*( self.const_LimitValue[i] -self.const_Value[i] )
        
        
    def evaluate_solution(self):
        '''
                        计算 当前这个个体对于各个函数的适应度
        '''
        self.TList= [0]*8
        
        for i in range(1,8):
            self.TList[i] =self.TList[i-1]+ self.attributes[i-1]
        self.BSplineCurve =  BSplineCurve(self.TList,7,self.pointList)
        
        self.BSplineCurve.CalBSplineCurve()
        self.objectives[0] = self.BSplineCurve.GetTall()  #时间最小
        self.objectives[1] = self.BSplineCurve.GetE_J_Level("J")  #最平滑
        self.objectives[2] = self.BSplineCurve.GetE_J_Level("E")  #能量最小
        self.evaluate_Infeasible_Degree()
       
    def crossover(self, other):
        '''
        Crossover of T1 solutions. 交叉
        '''
        child_solution = BSplineCurve7(self.const_LimitValue,self.pointList,self.attributes)
        
        for i in range( len(self.attributes) ):
            child_solution.attributes[i] = math.sqrt(self.attributes[i] * other.attributes[i])
        
        return child_solution
    
    def mutate(self):
        '''
        Mutation of T1 solution. 变异
        '''
        mutate_value = 0
        while mutate_value == 0.0:
            mutate_value = (random.random()*10)
        self.attributes[random.randint(0, len(self.attributes)-1)] = mutate_value
        
        
if __name__ == '__main__':
    nsga2 = NSGAII(3, 0.5, 0.7)
 
    mInit_TPopluation = Init_TPopluation(8,100)
     
    P_List1 = [43.35,
              43.33,
              50.04,
              62.67,
              78.04,
              94.40,
              104.13,
              111.91]
   
 
     
    TList = mInit_TPopluation.T_Population()
    P = []
    for i in range(20):
 
        P.append(BSplineCurve7( [100,45,60], P_List1,TList[i]))
 
    nsga2.run(P, 100,150)
      
    csv_file = open('nsga2_out.csv', 'w')
      
      
    for i in range(len(P)):
        csv_file.write("" + str(P[i].objectives[0]) + ", " + str(P[i].objectives[1]) +"\n")
          
    csv_file.close()
      
    import numpy as np
    import matplotlib.pyplot as plt
    from mayavi import mlab
    ListX= []
    ListY= []
    ListZ= []
    
    index =0
    var = 0 
    smin = 10000
    for e in P:
        
        if smin >  e.objectives[0]:
            smin = e.objectives[0]
            index= var
        var = var+1
        print "Time:"+str(e.objectives[0])+", 最平滑:"+str(e.objectives[1])+", 能量:"+str(e.objectives[2])+"\n"
    print smin,var
#         ListX.append(e.objectives[0]) 
#         ListY.append(e.objectives[1]*100) 
#         ListZ.append(e.objectives[2]*100) 
    
    
    DrawT_List = np.linspace(0, 1, 300)
    NewList=[]
    for t in DrawT_List:
        NewList.append(P[index].objectives[0]*t)
        
    plt.figure(figsize=(8,8))
    
    plt.plot(P[index].TList,P_List1,"b*",label="org_point",linewidth=5)
    plt.plot(NewList,P[index].BSplineCurve.GetT_PList(DrawT_List),"b-",label="point",color="red",linewidth=2)
    plt.plot(NewList,P[index].BSplineCurve.GetT_VList(DrawT_List),"b-",label="V",color="green",linewidth=2)
    plt.plot(NewList,P[index].BSplineCurve.GetT_AList(DrawT_List),"b-",label="A",color="black",linewidth=2)
    plt.plot(NewList,P[index].BSplineCurve.GetT_JList(DrawT_List),"b-",label="J",color="blue",linewidth=2)
    
    plt.xlabel("Time(s)")
    plt.ylabel("value")
    plt.ylim(-200,200)
    plt.legend()
    plt.show()
#     pl = mlab.surf(ListX, ListY, ListZ, warp_scale="auto")
#     mlab.axes(xlabel='Time', ylabel='J', zlabel='E')
#     mlab.outline(pl)
#     mlab.show()

        
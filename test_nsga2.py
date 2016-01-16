# _*_ coding:utf-8 _*_
'''
Created on 10/01/2011

@author: 04610922479
'''
import random, math
from nsga2 import Solution
from nsga2 import NSGAII

#from nsga2.nsga2 import Solution

class T1Solution(Solution):
    '''
    Solution for the T1 function.
    '''
    def __init__(self):
        '''
        Constructor.
        '''
        Solution.__init__(self, 2,3)
        
        self.xmin = 0.0
        self.xmax = 1.0
        
        self.const_LimitValue[0] = 15
        self.const_LimitValue[1] = 5
        self.const_LimitValue[2] = 2

        

        
        self.Infeasible_Degree = 0.0
        self.Infeasible_Degree_Threshold = 0.0
        
        for _ in range(30):
            self.attributes.append(random.random())

        self.evaluate_solution()
        
    def evaluate_solution(self):
        '''
        Implementation of method evaluate_solution() for T1 function.
        '''
        self.objectives[0] = self.attributes[0]
        
        self.sum = 0.0
        for i in range(30):
            self.sum += self.attributes[i]

            
        g = 1.0 + (9.0 * (self.sum / 29))
        
        self.objectives[1] = g * (1.0 - math.sqrt(self.attributes[0] / g))
        #self.objectives[1]= 1.0/self.attributes[0]
        
        self.const_Value[0] = self.sum
        self.const_Value[1] = self.objectives[1]
        self.const_Value[2] = self.objectives[0]

        

        
        for i in range(self.num_const):
            if ( self.const_LimitValue[i] -self.const_Value[i] ) > 0 :
                self.Infeasible_Degree += 0
            else:
                self.Infeasible_Degree += ( self.const_LimitValue[i] -self.const_Value[i] )*( self.const_LimitValue[i] -self.const_Value[i] )
        
    def crossover(self, other):
        '''
        Crossover of T1 solutions. 交叉
        '''
        child_solution = T1Solution()
        
        for i in range(30):
            child_solution.attributes[i] = math.sqrt(self.attributes[i] * other.attributes[i])
        
        return child_solution
    
    def mutate(self):
        '''
        Mutation of T1 solution. 变异
        '''
        self.attributes[random.randint(0, 29)] = random.random()

    
if __name__ == '__main__':
    nsga2 = NSGAII(2, 0.5, 0.7)
    
    P = []
    for i in range(100):
        P.append(T1Solution())
        
#    
#     
#     nsga2.run(P, 100,200)
#     
#     csv_file = open('nsga2_out.csv', 'w')
#     
#     
#     for i in range(len(P)):
#         csv_file.write("" + str(P[i].objectives[0]) + ", " + str(P[i].objectives[1]) +"\n")
#         
#     csv_file.close()
#     
#     import numpy as np
#     import matplotlib.pyplot as plt
#     ListX= []
#     ListY= []
#     for e in P:
#         ListX.append(e.objectives[0]) 
#         ListY.append(e.objectives[1]) 
#         print "sum:"+str(e.const_Value[0])+", objectives[1]:"+str(e.const_Value[1])+", objectives[0]:"+str(e.const_Value[2])+"\n"
#       
#     plt.figure(figsize=(8,8))
#     plt.plot(ListX,ListY,"b*",label="org_point",linewidth=5)
#     plt.legend()
#     plt.show()

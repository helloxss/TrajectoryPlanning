#_*_ coding:utf-8 _*_
'''
Created on 2016年1月20日

@author: bush2582
@email : bush2582@163.com
'''
from NSGA_II import NSGA_II
from Decorator_Package.Decorator_OtherDefine_NSGAII import Decorator_OtherDefine_NSGAII

class NSGA_II_With_Constraint(NSGA_II):
    '''
    NSGA_II算法，配合使用了约束
    '''
    Decorator_OtherDefine_NSGAII = Decorator_OtherDefine_NSGAII()

    def __init__(self,num_objectives, mutation_rate=0.1, crossover_rate=1.0,TargetPoint=[]):
        NSGA_II.__init__(self,num_objectives,mutation_rate,crossover_rate)
        NSGA_II.Is_Dominance_Handle         = self.Is_Dominance
        NSGA_II.Evolve_A_Generation_Handle  = self.Evolve_A_Generation
        NSGA_II.crowded_comparison_Handle   = self.crowded_comparison
        
        self.TargetPoint = TargetPoint
        
        self.Infeasible_Degree_Threshold = 0.0 #不可行度

    
    @Decorator_OtherDefine_NSGAII.Is_Violate_Constraint
    def Is_Dominance(self, Fir_Individual, Sec_Individual):    
        return NSGA_II.Is_Dominance(self, Fir_Individual, Sec_Individual)     
    
    @Decorator_OtherDefine_NSGAII.Cal_Infeasible_Degree_Threshold

    def Evolve_A_Generation(self, Generation, Population, population_size):       
        return NSGA_II.Evolve_A_Generation(self, Generation, Population, population_size)
    
    @Decorator_OtherDefine_NSGAII.Crowded_comparison_Constraint
    def crowded_comparison(self, s1, s2):
        return NSGA_II.crowded_comparison(self, s1, s2)
        
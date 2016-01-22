#_*_ coding:utf-8 _*_
'''
Created on 2016年1月20日

@author: bush2582
@email : bush2582@163.com
'''
from NSGA_II import NSGA_II
from Decorator_Package.Decorator_OtherDefine_NSGAII import Decorator_OtherDefine_NSGAII
class NSGA_II_With_Constraint_And_R_Dominance(NSGA_II):
    '''
    NSGA_II算法，配合使用了约束和R支配
    '''
    Decorator_OtherDefine_NSGAII = Decorator_OtherDefine_NSGAII()

    def __init__(self,num_objectives, mutation_rate=0.1, crossover_rate=1.0,TargetPoint=[]):
        '''
        function:初始化
        para：1、num_objectives 目标函数个数  2、mutation_rate 变异率  3、crossover_rate 交叉率 4、TargetPoint 目标点
        '''
        NSGA_II.__init__(self,num_objectives,mutation_rate,crossover_rate)
        NSGA_II.Is_Dominance_Handle         = self.Is_Dominance
        NSGA_II.Evolve_A_Generation_Handle  = self.Evolve_A_Generation
        NSGA_II.crowded_comparison_Handle   = self.crowded_comparison
        
        self.TargetPoint = TargetPoint
        self.Num_generations = -1
        
        self.Infeasible_Degree_Threshold = 0.0 #不可行度
        self.R_Dominance_Threshol = 0.0     #R支配阈值
        self.MaxR_Dist = 0.0
        self.MinR_Dist = 0.0
    
    @Decorator_OtherDefine_NSGAII.Is_Violate_Constraint
    @Decorator_OtherDefine_NSGAII.Is_R_Dominace
    def Is_Dominance(self, Fir_Individual, Sec_Individual):    
        return NSGA_II.Is_Dominance(self, Fir_Individual, Sec_Individual)     
    
    def run(self, Init_Population, population_size, num_generations):

        return NSGA_II.run(self, Init_Population, population_size, num_generations)
    
    @Decorator_OtherDefine_NSGAII.Cal_Infeasible_Degree_Threshold
    @Decorator_OtherDefine_NSGAII.Cal_R_Dominance_Threshol
    def Evolve_A_Generation(self, Generation, Population, population_size):       
        return NSGA_II.Evolve_A_Generation(self, Generation, Population, population_size)
    
    @Decorator_OtherDefine_NSGAII.Crowded_comparison_Constraint
    def crowded_comparison(self, s1, s2):
        return NSGA_II.crowded_comparison(self, s1, s2)
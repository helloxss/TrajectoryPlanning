# _*_ coding:utf-8 _*_
'''
Created on 2016年1月11日
作者：bush2582
邮箱：bush2582@163.com
'''
import numpy as np
import random 
class Init_TPopluation(object):
    '''
    classname: Init_TPopluation
    function:用一维  Logistic映射初始化时间向量T(现在暂时用的随机区间)
    '''
    def __init__(self, Init_T_PopulationScal,Init_PopulationScal):
        self.__T_PopulationScal = Init_T_PopulationScal
        self.__T_PopulationList = []
        RandomData = np.linspace(0.1,7, 100)
        
        #保留2位小数
        RandomData = self.__Round(RandomData, 2)

        
        Index = 0 
        while Index <Init_PopulationScal  :
            
            TmpList = random.sample(RandomData,Init_T_PopulationScal) 
            
             
            TmpList = self.__Round(TmpList, 2)
            TmpList.sort();
            
            self.__T_PopulationList.append(TmpList)
            Index=Index+1
        

            
    def T_Population(self):
        '''
        Methon    :T_Population
        Function  :返回初始化种群
        '''
        return self.__T_PopulationList
              
    def __Round(self,List,ReseverBit):
        RetList =[]
        '''
        MethonName  :__Round
        Function    :对list进行处理保留ReseverBit位小数
        Para        :1、List：需要被处理的list 2、ReseverBit：要保留的位数
        '''
        #保留两位小数
        for e in List:
            RetList.append( round(e,ReseverBit) )
        return RetList
 
if __name__ == '__main__':
    mLogistic_Map_T = Init_TPopluation(7,100)
    print mLogistic_Map_T.T_Population()
    
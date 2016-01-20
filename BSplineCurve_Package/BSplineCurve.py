# _*_ coding:utf-8 _*_
'''
Created on 2015年12月19日

@author    : Administrator
@function  : 非均匀K次B样条曲线类（好吧。。。我支持了7次(。・＿・。)ﾉ）
'''
import logging
from LoadConfig import Config
import numpy as np
import matplotlib.pyplot as plt
class BSplineCurve():

    __mT_List  = []
    __mU_List  = []
    __mP_Array = []
    __mP_OrgArray = []
    __mC_N_Array         = []
    __mControl_D_Array   = []
    __mConttol_D_Array_V = []
    __mConttol_D_Array_A = []
    __mConttol_D_Array_J = []
    __m_integration_Region_List = []
    __mK      = 0
    __mT_all  = 0
    __m_n     = 0
    
    
    '''
    @Name    : __init__
    @Para    : 1、self    : 
               2、TList   : 时间T参数列表
               3、K       : K次
    '''  
    def __init__(self, TList,K,PList):
        
        self.__mT_List  = []
        self.__mU_List  = []
        self.__mP_Array = []
        self.__mP_OrgArray = []
        self.__mC_N_Array         = []
        self.__mControl_D_Array   = []
        self.__mConttol_D_Array_V = []
        self.__mConttol_D_Array_A = []
        self.__mConttol_D_Array_J = []
        
        self.__mT_List = TList
        self.__mK = K
        self.__mT_all = TList[len(TList)-1] - TList[0]
        self.__m_n = len(TList)-1
        self.__m_integration_Region_List = np.linspace(0, 1, 50) #数值积分小区间
        
        logging.info(u"=============================================")
        logging.info(u">>now start cal and para will following that")
        logging.info(u">>-----------TList's each var--------------" )
        for index,e in enumerate(TList):
            logging.info(u">>Index %d's value:%f" ,index, e)
        logging.info(u">>------------------------------------------")
        logging.info(u">>-----------PList's each var--------------" )
        for index,e in enumerate(PList):
            logging.info(u">>Index %d's value:%f" ,index, e)
        logging.info(u">>------------------------------------------")
        logging.info(u">>Data's number is %d ",self.__m_n)
        logging.info(u">>K is %d ",self.__mK)
        logging.info(u">>T_all is %f ",self.__mT_all)
        logging.info(u"=============================================\n")
        
        #################处理坐标点矩阵################
        #self.__mP_OrgArray = PList
        for e in PList:
            Tmp_List =[e]
            self.__mP_Array.append(Tmp_List)
        
        i = 0 
        while i < K-1 :
            Tmp_List =[0]
            self.__mP_Array.append(Tmp_List)
            i = i+1
            
        self.__mP_Array = np.array(self.__mP_Array)

        #################处理坐标点矩阵################
        
    '''
    @Name    : Convert_T_To_U
    @Para    : 1、TList   : 时间T参数列表
               2、K       : K次
               3、IsR     : 是正确的日志信息
    @Function: 对输入的时间参数进行归一化到节点向量u
    '''  
    def __Convert_T_To_U(self,TList,K): 
        Ret_UList = []
        DisTList  = []      #时间间隔的列表
        Ret_U_List_Index = 0 
        Sum_DisT = 0        #时间间隔的总和
        All_T = TList[len(TList)-1] - TList[0]
        logging.info(u">>Cal_u-1 Step Done. All_T's value :%f" , All_T)
        
        #计算 各个时间的时间间隔以及时间间隔的总和 ，为归一化做准备
        for T in TList:
            CurrnetIndex = TList.index(T)
            if CurrnetIndex == len(TList)-1: break
            DisTList.append(TList[CurrnetIndex+1] - T)
        
        for DisT in DisTList:
            Sum_DisT = Sum_DisT + DisT
            
        logging.info(u">>Cal_u-2 Step Done. SumTList's value :%d" , Sum_DisT)
        
        #初始化u(0) 至 u(k)
        while Ret_U_List_Index <= K:
            Ret_UList.append(0) 
            Ret_U_List_Index += 1
        
        #初始化u(k+1) 至 u(n+k-1)
        while Ret_U_List_Index <= K+len(TList)-1 : #从 k+1 至 n+k-1
            TmpT = ( DisTList[Ret_U_List_Index-K-1]*1.0 ) /Sum_DisT #dis(i-k-1)/all
            Ret_UList.append( Ret_UList[Ret_U_List_Index-1]+  TmpT)
            Ret_U_List_Index += 1
            
        #初始化u(k+n) 至 u(n+2k)
        while Ret_U_List_Index < 2*K+len(TList) :
            Ret_UList.append(1) 
            Ret_U_List_Index += 1
            
        logging.info(u">>Cal_u-3 Step Done. Ret_UList's len :%d" , len(Ret_UList))
        
        logging.info(u">>-----------Ret_UList's each var----------" )
        for index,e in enumerate(Ret_UList):
                logging.info(u">>Index %d's value:%f" ,index, e)
        logging.info(u">>-----------------------------------------" )
        
        return Ret_UList
    
    '''
    @Name    : __CalN
    @Para    : 1、i       : u在向量列表中的区间的位置，其为区间左端的值
               2、u       : u值
               3、U       : 向量列表
    @Function: 计算k次非均匀有理B样条曲线基函数
    '''  
    def  __CalN(self,i,u,U,K):
        j=1
        left = []
        N = []
        rigth = []
        left.append(0)
        N.append(1.0)
        rigth.append(0)
        
        while  j<=K :
            left.append( u-U[i+1-j])
            rigth.append( U[i+j] - u )
            save = 0.0
            r = 0
            while r < j :
                temp = (N[r]*1.0) /(rigth[r+1] + left[j-r] )
                N[r]= ( save + rigth[r+1]* temp)
                save = left[j-r]*temp
                r =r+1
            N.append(save)
            j+=1
        
        return N 
        
    '''
    @Name    : __CreateC_N
    @Para    : 
    @Function: 计算CN矩阵
    '''  
    def __CreateC_N(self):
        
        C_N = []
        Index_I =0
        while Index_I < (self.__m_n+7):
            listTmp = [0]*(self.__m_n+7)
            
            if Index_I == 0 :
                listTmp[0] =1.0

            elif Index_I ==  self.__m_n :
                listTmp[self.__m_n+6] =1.0

            elif Index_I >= 1 and Index_I <=  self.__m_n-1 :
                
                Index_J = Index_I
                ret = self.__CalN(Index_J+self.__mK-1,
                                  self.__mU_List[Index_J+self.__mK],
                                  self.__mU_List,
                                  self.__mK)
 
                for index ,e in enumerate(ret) :
                    listTmp[index+Index_J-1] = ret[index]
            C_N.append(listTmp)
            Index_I += 1  
        
        ##计算 一阶 二阶 三阶方程
        C_sv1 = -7.0 * ( 1.0/(self.__mU_List[8]-self.__mU_List[1]) ) / self.__mT_all
        C_sv2 =  7.0 * ( 1.0/(self.__mU_List[8]-self.__mU_List[1]) ) / self.__mT_all
        
        C_ev1 = -7.0 * ( 1.0/(self.__mU_List[self.__m_n+13]-self.__mU_List[self.__m_n+6]) ) / self.__mT_all
        C_ev2 =  7.0 * ( 1.0/(self.__mU_List[self.__m_n+13]-self.__mU_List[self.__m_n+6]) ) / self.__mT_all
        
        C_sa1 =  42  * ( 1.0/( (self.__mU_List[8]-self.__mU_List[2])*(self.__mU_List[8]-self.__mU_List[1]) ) 
                       ) / ( (self.__mT_all)*(self.__mT_all) )
                       
        C_sa2 = -42  * ( ( 1.0/( (self.__mU_List[8]-self.__mU_List[2])*(self.__mU_List[9]-self.__mU_List[2]) ) ) + 
                         ( 1.0/( (self.__mU_List[8]-self.__mU_List[2])*(self.__mU_List[8]-self.__mU_List[1]) ) )  
                       ) /  ( (self.__mT_all)*(self.__mT_all) )
        C_sa3 =  42  * (
                         1.0/( (self.__mU_List[8]-self.__mU_List[2])*(self.__mU_List[9]-self.__mU_List[2]) )
                       ) /  ( (self.__mT_all)*(self.__mT_all) )  
        
        C_ea1 =  42  * (
                         1.0/( (self.__mU_List[self.__m_n+12]-self.__mU_List[self.__m_n+6])*
                               (self.__mU_List[self.__m_n+12]-self.__mU_List[self.__m_n+5]) 
                             )
                       ) /  ( (self.__mT_all)*(self.__mT_all) ) 
                       
        C_ea2 = -42  * ( ( 1.0/( (self.__mU_List[self.__m_n+12]-self.__mU_List[self.__m_n+6])*
                                 (self.__mU_List[self.__m_n+13]-self.__mU_List[self.__m_n+6]) 
                                ) 
                         ) + 
                         ( 1.0/( (self.__mU_List[self.__m_n+12]-self.__mU_List[self.__m_n+6])*
                                 (self.__mU_List[self.__m_n+12]-self.__mU_List[self.__m_n+5]) 
                                ) 
                         )  
                       ) /  ( (self.__mT_all)*(self.__mT_all) )   
        
        C_ea3 =  42  * (
                         1.0/( 
                               (self.__mU_List[self.__m_n+12]-self.__mU_List[self.__m_n+6])*
                               (self.__mU_List[self.__m_n+13]-self.__mU_List[self.__m_n+6]) 
                             )
                       ) /  ( (self.__mT_all)*(self.__mT_all) )        
        
        C_sj1 = -210 * ( 1.0/( 
                              (self.__mU_List[8]-self.__mU_List[3])*
                              (self.__mU_List[8]-self.__mU_List[2])*
                              (self.__mU_List[8]-self.__mU_List[1]) 
                             ) 
                        ) /  ( (self.__mT_all)*(self.__mT_all)*(self.__mT_all) )
        
        C_sj2 =  210 * (
                           1.0/ ( (self.__mU_List[8]-self.__mU_List[3])*
                                  (self.__mU_List[9]-self.__mU_List[3])*
                                  (self.__mU_List[9]-self.__mU_List[2]) 
                                )+
                           1.0/ ( (self.__mU_List[8]-self.__mU_List[3])*
                                  (self.__mU_List[8]-self.__mU_List[2])*
                                  (self.__mU_List[9]-self.__mU_List[2]) 
                                )+
                           1.0/ ( (self.__mU_List[8]-self.__mU_List[3])*
                                  (self.__mU_List[8]-self.__mU_List[2])*
                                  (self.__mU_List[8]-self.__mU_List[1]) 
                                )    
                        ) /  ( (self.__mT_all)*(self.__mT_all)*(self.__mT_all) )
                        
        C_sj3 = -210 * (
                           1.0/ ( (self.__mU_List[8]-self.__mU_List[3])*
                                  (self.__mU_List[9]-self.__mU_List[3])*
                                  (self.__mU_List[10]-self.__mU_List[3]) 
                                )+
                           1.0/ ( (self.__mU_List[8]-self.__mU_List[3])*
                                  (self.__mU_List[9]-self.__mU_List[3])*
                                  (self.__mU_List[9]-self.__mU_List[2]) 
                                )+
                           1.0/ ( (self.__mU_List[8]-self.__mU_List[3])*
                                  (self.__mU_List[8]-self.__mU_List[2])*
                                  (self.__mU_List[9]-self.__mU_List[2]) 
                                )
                        ) /  ( (self.__mT_all)*(self.__mT_all)*(self.__mT_all) )
        
        C_sj4 =  210 * ( 1.0/( 
                              (self.__mU_List[8]-self.__mU_List[3])*
                              (self.__mU_List[9]-self.__mU_List[3])*
                              (self.__mU_List[10]-self.__mU_List[3]) 
                             ) 
                        ) /  ( (self.__mT_all)*(self.__mT_all)*(self.__mT_all) )
        
        C_ej1 = -210 * ( 1.0/( 
                              (self.__mU_List[self.__m_n+11]-self.__mU_List[self.__m_n+6])*
                              (self.__mU_List[self.__m_n+11]-self.__mU_List[self.__m_n+5])*
                              (self.__mU_List[self.__m_n+11]-self.__mU_List[self.__m_n+4]) 
                             ) 
                        ) /  ( (self.__mT_all)*(self.__mT_all)*(self.__mT_all) )
        
        C_ej2 =  210 * (      
                           1.0/ ( (self.__mU_List[self.__m_n+11]-self.__mU_List[self.__m_n+6])*
                                  (self.__mU_List[self.__m_n+12]-self.__mU_List[self.__m_n+6])*
                                  (self.__mU_List[self.__m_n+12]-self.__mU_List[self.__m_n+5]) 
                                )+
                           1.0/ ( (self.__mU_List[self.__m_n+11]-self.__mU_List[self.__m_n+6])*
                                  (self.__mU_List[self.__m_n+11]-self.__mU_List[self.__m_n+5])*
                                  (self.__mU_List[self.__m_n+12]-self.__mU_List[self.__m_n+5]) 
                                )+
                           1.0/ ( (self.__mU_List[self.__m_n+11]-self.__mU_List[self.__m_n+6])*
                                  (self.__mU_List[self.__m_n+11]-self.__mU_List[self.__m_n+5])*
                                  (self.__mU_List[self.__m_n+11]-self.__mU_List[self.__m_n+4]) 
                                )     
                        ) /  ( (self.__mT_all)*(self.__mT_all)*(self.__mT_all) )
                        
        C_ej3 = -210 * (

                           1.0/ ( (self.__mU_List[self.__m_n+11]-self.__mU_List[self.__m_n+6])*
                                  (self.__mU_List[self.__m_n+12]-self.__mU_List[self.__m_n+6])*
                                  (self.__mU_List[self.__m_n+13]-self.__mU_List[self.__m_n+6]) 
                                )+
                           1.0/ ( (self.__mU_List[self.__m_n+11]-self.__mU_List[self.__m_n+6])*
                                  (self.__mU_List[self.__m_n+12]-self.__mU_List[self.__m_n+6])*
                                  (self.__mU_List[self.__m_n+12]-self.__mU_List[self.__m_n+5]) 
                                )+
                           1.0/ ( (self.__mU_List[self.__m_n+11]-self.__mU_List[self.__m_n+6])*
                                  (self.__mU_List[self.__m_n+11]-self.__mU_List[self.__m_n+5])*
                                  (self.__mU_List[self.__m_n+12]-self.__mU_List[self.__m_n+5]) 
                                )
                        ) /  ( (self.__mT_all)*(self.__mT_all)*(self.__mT_all) )
        
        C_ej4 =  210 * ( 1.0/( 
                              (self.__mU_List[self.__m_n+11]-self.__mU_List[self.__m_n+6])*
                              (self.__mU_List[self.__m_n+12]-self.__mU_List[self.__m_n+6])*
                              (self.__mU_List[self.__m_n+13]-self.__mU_List[self.__m_n+6]) 
                             ) 
                        ) /  ( (self.__mT_all)*(self.__mT_all)*(self.__mT_all) )
        
        
        C_N[self.__m_n+1][0] = C_sv1
        C_N[self.__m_n+1][1] = C_sv2
        
        C_N[self.__m_n+2][self.__m_n+self.__mK-1-1] = C_ev1
        C_N[self.__m_n+2][self.__m_n+self.__mK-1]   = C_ev2
        
        C_N[self.__m_n+3][0] = C_sa1
        C_N[self.__m_n+3][1] = C_sa2
        C_N[self.__m_n+3][2] = C_sa3
        
        C_N[self.__m_n+4][self.__m_n+self.__mK-1-2] = C_ea1
        C_N[self.__m_n+4][self.__m_n+self.__mK-1-1] = C_ea2
        C_N[self.__m_n+4][self.__m_n+self.__mK-1]   = C_ea3
        
        C_N[self.__m_n+5][0] = C_sj1
        C_N[self.__m_n+5][1] = C_sj2
        C_N[self.__m_n+5][2] = C_sj3
        C_N[self.__m_n+5][3] = C_sj4
        
        C_N[self.__m_n+6][self.__m_n+self.__mK-1-3] = C_ej1
        C_N[self.__m_n+6][self.__m_n+self.__mK-1-2] = C_ej2
        C_N[self.__m_n+6][self.__m_n+self.__mK-1-1] = C_ej3
        C_N[self.__m_n+6][self.__m_n+self.__mK-1]   = C_ej4
        
        self.__mC_N_Array = np.array(C_N)  

        self.__mControl_D_Array = np.dot(np.linalg.inv(self.__mC_N_Array),self.__mP_Array)
        self.__GetVControl();
        self.__GetAControl();
        self.__GetJControl();
        
        logging.info(u">>Cal ControlPoint Done.")   
        logging.info(u">>----------Control_D_Array's each var-----------" )
        for index,e in enumerate( self.__mControl_D_Array):
            logging.info(u">>Index %d's value:%f" ,index, e)

        logging.info(u">>----------------------------------------------" )
        
        pass
    
    '''
    @Name    : __SearchIndex
    @Para    : 1、u：u值
    @Function: 查找u在ulist中所处的区间，返回区间左下角值
    '''  
    def __SearchIndex(self,u):
        Left = self.__mK
        Right = self.__m_n+self.__mK
        Mid = (Left + Right)/2
 
        #print u, self.__mU_List[self.__m_n+self.__mK] 
       
        if u == self.__mU_List[self.__m_n+self.__mK]: return self.__m_n+self.__mK-1
        if u == 1.0: return self.__m_n+self.__mK-1  #保证1.0这个点事不会死循环
         
        while  u < self.__mU_List[Mid] or u >= self.__mU_List[Mid+1] :
            if u < self.__mU_List[Mid]:
                Right = Mid 
            else :
                Left = Mid
            Mid = (Left + Right)/2 
           
        return Mid


    '''
    @Name    : __GetJControl
    @Para    : 
    @Function: 计算加加速度控制点
    ''' 
    def __GetJControl(self):
        self.__mConttol_D_Array_J =[]
        i = 3
        while i < (self.__m_n+self.__mK):
            tmp = ( self.__mK-2) *                                                      \
                  ( self.__mConttol_D_Array_A[i-2]-self.__mConttol_D_Array_A[i-3] )/    \
                  ( self.__mU_List[i+self.__mK-2] - self.__mU_List[i] )
            self.__mConttol_D_Array_J.append(tmp/self.__mT_all)#这里要除以时间跨度
            i+=1
    
    '''
    @Name    : __GetAControl
    @Para    : 
    @Function: 计算加速度控制点
    ''' 
    def __GetAControl(self):
        self.__mConttol_D_Array_A =[]
        i = 2
        while i < (self.__m_n+self.__mK):
            tmp = ( self.__mK-1) *                                                      \
                  ( self.__mConttol_D_Array_V[i-1]-self.__mConttol_D_Array_V[i-2] )/    \
                  ( self.__mU_List[i+self.__mK-1] - self.__mU_List[i] )
            self.__mConttol_D_Array_A.append(tmp/self.__mT_all)#这里要除以时间跨度
            i+=1
            
    '''
    @Name    : __GetVControl
    @Para    : 
    @Function: 计算速度控制点
    ''' 
    def __GetVControl(self):
        self.__mConttol_D_Array_V =[]
        i = 1
        while i < (self.__m_n+self.__mK):
            tmp = ( self.__mK) *                                                \
                  ( self.__mControl_D_Array[i]-self.__mControl_D_Array[i-1] )/  \
                  ( self.__mU_List[i+self.__mK] - self.__mU_List[i] )
            self.__mConttol_D_Array_V.append(tmp/self.__mT_all)#这里要除以时间跨度
            i+=1
    
    '''
    @Name    : __Get_JPoint
    @Para    : 1、T：时间点
    @Function: 获得某一时刻的加加速度值
    '''          
    def __Get_JPoint(self,T): 
        IndexT = self.__SearchIndex(T)

        PointRet = 0.0
        C_NRet = self.__CalN(IndexT,T,self.__mU_List,self.__mK-3)

        for index_CN,e in enumerate(C_NRet):
            PointRet += self.__mConttol_D_Array_J[IndexT-self.__mK+index_CN]*e
        return PointRet
    
    '''
    @Name    : __Get_APoint
    @Para    : 1、T：时间点
    @Function: 获得某一时刻的加速度值
    '''          
    def __Get_APoint(self,T):
        IndexT = self.__SearchIndex(T)
        PointRet = 0.0
        C_NRet = self.__CalN(IndexT,T,self.__mU_List,self.__mK-2)

        for index_CN,e in enumerate(C_NRet):
            PointRet += self.__mConttol_D_Array_A[IndexT-self.__mK+index_CN]*e
        return PointRet
    
    '''
    @Name    : __Get_VPoint
    @Para    : 1、T：时间点
    @Function: 获得某一时刻的速度值
    '''          
    def __Get_VPoint(self,T):
        IndexT = self.__SearchIndex(T)
        PointRet = 0.0
        C_NRet = self.__CalN(IndexT,T,self.__mU_List,self.__mK-1)
        for index_CN,e in enumerate(C_NRet):
            PointRet += self.__mConttol_D_Array_V[IndexT-self.__mK+index_CN]*e
        return PointRet
        
    '''
    @Name    : __Get_Point
    @Para    : 1、T：时间点
    @Function: 获得某一时刻的角度值
    '''  
    def __Get_Point(self,T):
        IndexT = self.__SearchIndex(T)
        PointRet = 0.0
        C_NRet = self.__CalN(IndexT,
                             T,
                             self.__mU_List,
                             self.__mK)
        for index_CN,e in enumerate(C_NRet):
            PointRet += self.__mControl_D_Array[IndexT-self.__mK+index_CN]*e
        return PointRet
    
    '''
    @Name    : GetMaxD_Control
    @Para    : 1、V_A_J:是V还是A还是Z
    @Function: 获得制点最大的顶点值（需要指定是哪种控制顶点）
    '''
    def GetMaxD_Control(self,V_A_J):
        MaxD = 0
        List=[]
        if V_A_J == "V":
            List=self.__mConttol_D_Array_V
        elif V_A_J == "A":
            List=self.__mConttol_D_Array_A
        elif V_A_J == "J":
            List=self.__mConttol_D_Array_J
            
        for index ,e in enumerate(List):
            
            if index == 0:
                MaxD = abs(e)
                continue
            elif abs(e) > MaxD:
                MaxD = abs(e)     
                
        logging.info(u">>MAX_Control_D_%s is %f ",V_A_J,MaxD)           
        return MaxD
    
    
    '''
    @Name    : GetT_PList
    @Para    : 1、TList：时间轴点
    @Function: 获得角度曲线列表
    '''  
    def GetT_PList(self,TList):
        Y_List = []
        for e in TList:
            Y_List.append( self.__Get_Point(e) )
        return Y_List
    
    '''
    @Name    : GetT_VList
    @Para    : 1、TList：时间轴点
    @Function: 获得速度曲线列表
    '''  
    def GetT_VList(self,TList):
       
        V_List = []
        for e in TList:
            V_List.append( self.__Get_VPoint(e) )
        return V_List
    
    '''
    @Name    : GetT_AList
    @Para    : 1、TList：时间轴点
    @Function: 获得加速度曲线列表
    '''  
    def GetT_AList(self,TList):
       
        A_List = []
        for e in TList:
            A_List.append( self.__Get_APoint(e) )
        return A_List
    
    '''
    @Name    : GetT_JList
    @Para    : 1、TList：时间轴点
    @Function: 获得加加速度曲线列表
    '''  
    def GetT_JList(self,TList):
       
        J_List = []

        for e in TList:

            J_List.append( self.__Get_JPoint(e) )
  
        return J_List
    
    '''
    @Name    : GetE_J_Level
    @Para    : 
    @Function: 获得能量或平滑指数
    ''' 
    def GetE_J_Level(self,J_E):
        
        
        A_List = []
        if J_E == "J" :
            A_List = self.GetT_JList(self.__m_integration_Region_List)
        elif J_E == "E":
            A_List = self.GetT_AList(self.__m_integration_Region_List)

        
        h = self.__m_integration_Region_List[1]-self.__m_integration_Region_List[0]
        s = (A_List[0]+A_List[len(A_List)-1])/2
        
        
        for index,e in enumerate(A_List):
            if index == 0  : continue
            elif index == len(A_List)-1 :break
            s += ( e*e )

        return (h*s)/(self.__mT_all)
      
    '''
    @Name    : GetTall
    @Para    : 
    @Function: 获得运动时间
    '''  
    def GetTall(self):
        return self.__mT_all
     
    '''
    @Name    : CalBSplineCurve
    @Para    : 
    @Function: 计算B样条曲线
    '''  
    def CalBSplineCurve(self):
        
        logging.info(u"=============================================")
        self.__mU_List = self.__Convert_T_To_U(self.__mT_List,self.__mK)
        self.__CreateC_N()
        logging.info(u"=============================================\n")
        
        pass
        
    
if __name__ == '__main__':
    
    TList=[0,4.71,8.11,9.03,9.73,10.67,11.24,15.18]
    #TList=[0,5.8102,9.9533,11.5372,12.5419,13.7486,14.4987,18.6001]
    DrawT_List = np.linspace(0, 1, 300)
    
    
    
    P_List1 = [43.35,
              43.33,
              50.04,
              62.67,
              78.04,
              94.40,
              104.13,
              111.91]
    P_List2 = [130.57,
              152.09,
              170.66,
              179.41,
              182.70,
              178.45,
              173.54,
              132.80]
    P_List3 = [7.37,
              -18,
              -41.85,
              -53.76,
              -57.32,
              -52.73,
              -42.46,
              6.79]
    
    P_List4 = [39.06,
              45.09,
              51.19,
              53.59,
              54.62,
              53.38,
              50.33,
              40.41]
    
    P_List5 = [-46.66,
              48.02,
              -32.35,
              -4.99,
              33.04,
              75.94,
              94.76,
              112.16]

    List = P_List3
    
    mBSplineCurve1 = BSplineCurve(TList,7,List)
    mBSplineCurve1.CalBSplineCurve() 
    print mBSplineCurve1.GetE_J_Level("J")
    print mBSplineCurve1.GetE_J_Level("E")
    

    NewList=[]
    for e in DrawT_List:
        NewList.append(15.18*e)
        
    
    plt.figure(figsize=(8,8))
    plt.plot(TList,List,"b*",label="org_point",linewidth=5)
    plt.plot(NewList,mBSplineCurve1.GetT_PList(DrawT_List),"b-",label="point",color="red",linewidth=2)
    plt.plot(NewList,mBSplineCurve1.GetT_VList(DrawT_List),"b-",label="V",color="green",linewidth=2)
    plt.plot(NewList,mBSplineCurve1.GetT_AList(DrawT_List),"b-",label="A",color="black",linewidth=2)
    plt.plot(NewList,mBSplineCurve1.GetT_JList(DrawT_List),"b-",label="J",color="blue",linewidth=2)
    
    plt.xlabel("Time(s)")
    plt.ylabel("value")
    plt.ylim(-200,200)
    plt.legend()
    plt.show()
    
    
    
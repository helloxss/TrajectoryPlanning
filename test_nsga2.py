# _*_ coding:utf-8 _*_
'''
Created on 10/01/2011

@author: 04610922479
'''


#from nsga2.nsga2 import Solution

class MyApp():
    def __init__(self):
        self.func_map = {}
 
    def register(self,func):
        def wrapper(*args, **kw):
            
            args[0].AA = 1
            print args[0].AA
            func(*args, **kw)
        return wrapper

 
    def call_method(self,func):
        def wrapper(*args, **kw):

            
            if func(*args, **kw) == False:
                args[0].AA = 10
                print args[0].AA
            
        return wrapper

class A():
    m = MyApp()
    def __init__(self):
        
        pass
    
    @m.register
    @m.call_method
    def now(self,s):
        
        return True
        pass





    
if __name__ == '__main__':
    ma = A()
    ma.now("dd")

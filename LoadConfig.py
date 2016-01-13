# coding=utf-8
'''
Created on 2015年11月5日

@author: Administrator
'''

import logging;

class Config:

    @staticmethod
    def ConfigMonitorLog():
        logging.basicConfig(
                        level    = logging.INFO,
                        format   = 'LINE %(lineno)-4d  %(levelname)-8s %(message)s',
                        datefmt  = '%m-%d %H:%M',
                        filename = 'Log.txt',
                        filemode = 'w');
        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.StreamHandler();
        console.setLevel(logging.INFO);
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(message)s');
        # tell the handler to use this format
        console.setFormatter(formatter);
        logging.getLogger('').addHandler(console);
    
        

Config.ConfigMonitorLog()

if __name__ == '__main__':
    mConfig = Config()
    print mConfig.OurSysChartSet()
    if bool(mConfig.IsWriteToFile()) == True:
        print 1
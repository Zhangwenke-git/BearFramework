# coding=utf-8

import time
from datetime import datetime
from threading import Timer

from tools.ReadConfig import ReadConfig
from tools import logger
from config.settings import Settings
logger = logger.Logger("TimedTask")

class TimedTask(object):

    def timeCompare(self,time1,time2):
        """
        :function:比较两个时间点的前后，格式为字符串
        :param time1: string
        :param time2: string
        :return:
        """
        expired_flag=True
        defference = datetime.strptime(time1,"%Y-%m-%d %H:%M:%S") -  datetime.strptime(time2,"%Y-%m-%d %H:%M:%S")
        if defference.days>=0:
            logger.error('Timing task expired')
        else:
            logger.info(f'The timed task will be executed at :{time2}')
            logger.info('Now,pending...')
            expired_flag=False
        return expired_flag


    def executeTimedTask(self,seconds,task,parameter=()):
        """
        :function:传输函数，并获取config文件中的定时点，之后执行函数task,参数为parameter
        :param seconds: 延迟执行秒数
        :param task: 函数名称，无（）
        :param parameter: task函数的入参
        """
        if Settings.allowTimedTask:
            logger.info('Prepare to execute timed task!')
            current = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            timer = ReadConfig.getTimer()
            if not self.timeCompare(current,timer):
                while datetime.now().strftime("%Y-%m-%d %H:%M:%S")<=timer:
                    print(f'The current time is: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")},and timed point is: {timer}')
                    time.sleep(5)
                else:
                    logger.info(f'Prepare to execute task [{task.__name__}] at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
                    Timer(int(seconds), task, parameter).start()
        else:
            Timer(int(seconds), task, parameter).start()

if __name__ == '__main__':
    def task():
        print('Test!!!!')
    time_obj = TimedTask()
    time_obj.executeTimedTask(1,task=task)

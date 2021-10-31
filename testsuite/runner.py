import threading
import glob
import pytest
from config.settings import Settings
from tools.logger import Logger
from lib.core.CaseCreate import creation
from tools.TaskTimer import TimedTask
from tools.ReadConfig import ReadConfig

logger = Logger("runner")

def execute(data_mapping_dict):
    """
    执行整个pytest框架的主入口
    @param data_mapping_dict: 格式如data/case.py中的data_mapping_dict
    @return: 执行的过程中是否有错误出现
    """
    flag = False
    try:
        cond = threading.Condition()

        def run():
            cond.acquire()
            cond.wait()
            if ReadConfig.getReportStyle() == "AllureReport":
                pytest.main(['-s', '-q', '--alluredir', Settings.api_report_xml_path])
            else:
                pytest.main(['--junit-xml=%s/JunitXml.xml' % Settings.api_ant_report_path])
            cond.release()

        def createPyFile():
            cond.acquire()
            cond.notify()
            if len(glob.glob("test_*.py")) == 0:
                logger.info("Success to create API test case!")
                creation(data_mapping_dict)
            else:
                logger.info("Testcases have already exist!")
            cond.release()

        time_obj = TimedTask()
        time_obj.executeTimedTask(0, run)

        t_execute = threading.Thread(target=run)
        t_create = threading.Thread(target=createPyFile)

        for t in [t_execute,t_create]:
            t.setDaemon(True)
            t.start()

        for t in [t_execute, t_create]:#主线程等待子线程
            t.join()


    except Exception as e:
        logger.error(f"Fail to execute case,error as follows:{str(e)}")
    else:
        flag=True
        logger.info(f"Success to execute case!")
    finally:
        return flag


if __name__ == "__main__":
    from data.case import data_mapping_dict
    execute(data_mapping_dict)
import threading
import glob
import pytest
from config.settings import Settings
from tools.logger import Logger
from lib.core.CaseCreate import creation
from tools.TaskTimer import TimedTask
from tools.ReadConfig import ReadConfig

logger = Logger("runner")

def run(data_mapping_dict):
    cond = threading.Condition()

    def execute():
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
    time_obj.executeTimedTask(0, execute)

    t_execute = threading.Thread(target=execute)
    t_create = threading.Thread(target=createPyFile)

    t_execute.start()
    t_create.start()


if __name__ == "__main__":
    from data.case import data_mapping_dict
    run(data_mapping_dict)
# coding=utf-8

import threading
import glob
import pytest
from config.settings import Settings
from tools.logger import Logger
from lib.core.CaseCreate import creation
from tools.TaskTimer import TimedTask
from tools.ReadConfig import ReadConfig
from tools.ColorUtils import Color
from lib.ant.Template import AntReport

logger = Logger("runner")


class PytestExecution(object):

    def __init__(self):
        pass


    def execute(self, data_mapping_dict):
        """
        执行的pytest框架的主入口
        @param data_mapping_dict:
        @return:
        """
        flag = False
        summary = None
        try:
            cond = threading.Condition()

            def run():
                cond.acquire()
                cond.wait()
                if ReadConfig.getReportStyle() == "AllureReport":
                    pytest.main(['-v', '--alluredir', Settings.api_report_xml_path])
                else:
                    from tools.DosOrderUtils import DosCmd
                    pytest_order = "py.test -v --junit-xml=%s/JunitXml.xml --log-cli-level=INFO" % Settings.api_ant_report_path
                    dos_obj = DosCmd()
                    dos_obj.excute_cmd(pytest_order)
                    if ReadConfig.getReportStyle() == "AllureReport":
                        Color.green("====================================准备生成allure测试报告====================================")
                        DosCmd().excute_bat(Settings.generate_allure_api_report_bat)
                    elif ReadConfig.getReportStyle() == "AntReport":
                        Color.green("====================================准备生成Ant测试报告====================================")
                        nonlocal summary
                        summary = AntReport().antReport(Settings.api_ant_report_path)
                cond.release()

            def createPyFile():
                cond.acquire()
                cond.notify()
                if len(glob.glob("test_*.py")) == 0:
                    creation(data_mapping_dict)
                    logger.info("Success to create API test case!")
                else:
                    logger.info("Testcases have already exist!")
                cond.release()

            time_obj = TimedTask()
            time_obj.executeTimedTask(0, run)

            t_execute = threading.Thread(target=run)
            t_create = threading.Thread(target=createPyFile)

            for t in [t_execute, t_create]:
                t.start()

            for t in [t_execute, t_create]:  # 主线程等待子线程
                t.join()

        except Exception as e:
            logger.error(f"Fail to execute case,error as follows:{str(e)}")
        else:
            flag = True
            logger.info(f"Success to execute case!")
        finally:
            return flag,summary


def yield_pytest_exe():
    pytest_exe_obj = PytestExecution()
    yield pytest_exe_obj
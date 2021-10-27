# coding=utf-8

import pytest
import threading
import glob
from tools.logger import Logger
from lib.core.formateParm import JsonTemplateReader
from lib.core.CaseCreate import creation
from tools.TaskTimer import TimedTask
from tools import InitConfig
from tools.ColorUtils import Color
from tools.DosOrderUtils import DosCmd
from lib.ant.Template import AntReport
from config.settings import Settings
from tools.ReadConfig import ReadConfig
from data.case import data_mapping_dict
logger = Logger("APIconftest")


@pytest.fixture(scope="function")
def json_template(request):
    """
    :function:自动读取json模板
    :param request:
    :return:
    """

    def read_template_by_test_name(**kwargs):
        return JsonTemplateReader().get_data(request.function.__name__, **kwargs)
    return read_template_by_test_name


@pytest.fixture(scope="session", autouse=True)
def initEnvConf():
    """
    :function:初始化环境信息，生成xml文件，在allure报告中显示
    """
    initObj = InitConfig.Init_Env()
    initObj.init(Settings.api_env_path)


def pytest_sessionstart(session):
    """
    :function:开始前创建用例py文件，等初始化信息
    :param session:
    """
    from tools.FileUtils import FileUtils
    file = FileUtils()
    string = r"""
cd /d %~dp0
allure generate {base_dir}\report\allure\{parent}\{child}\xml -o {base_dir}\report\allure\{parent}\{child}\html --clean
    """ .format (base_dir=Settings.base_dir,parent=Settings.parent_folder,child = Settings.child_folder)
    file.createBatFile(string,Settings.generate_allure_api_report_bat)



def pytest_sessionfinish(session):
    """
    :function:测试结束后，添加结尾信息，例如生成测试报告
    :param session:
    """
    # if Settings.APIcaseFileRemove:
    #     from lib.core.CaseCreate import clear_pyfile
    #     clear_pyfile()

    if ReadConfig.getReportStyle() == "AllureReport":
        Color.green("====================================准备生成allure测试报告====================================")
        DosCmd().excute_bat(Settings.generate_allure_api_report_bat)
    elif ReadConfig.getReportStyle() == "AntReport":
        Color.green("====================================准备生成Ant测试报告====================================")
        AntReport().antReport(Settings.api_ant_report_path)



@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
　　每个测试用例执行后，制作测试报告
　　:param item:测试用例对象
　　:param call:测试用例的测试步骤
　　         执行完常规钩子函数返回的report报告有个属性叫report.when
            先执行when=’setup’ 返回setup 的执行结果
            然后执行when=’call’ 返回call 的执行结果
            最后执行when=’teardown’返回teardown 的执行结果
　　:return:
　　"""
    out = yield
    report = out.get_result()
    if report.when == "call":
        nodeid = report.nodeid
        outcome = report.outcome
        description = item.__doc__


@pytest.fixture(scope="function", autouse=True)
def add_extra_attribute(record_xml_attribute):
    record_xml_attribute("tester", "zhangwenke")


@pytest.fixture(scope="function", autouse=True)
def add_extra_property(record_property, caplog):
    record_property("outcome", 111)
    record_property("log", caplog)




# if __name__ == "__main__":
#     run(data_mapping_dict)
    #pytest.main(["-s","-q","--alluredir","../report/allure"])


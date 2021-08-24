# -*-coding=utf8-*-
import os
from tools.TimeUtil import TimeUtils


class Settings:
    parent_folder = TimeUtils.time8
    child_folder = TimeUtils.time9

    APIcaseFileRemove = False
    ReportAfterClose = True
    allowTimedTask = True

    success_flag = '通过'
    fail_flag = '失败'

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_path = os.path.join(base_dir, 'log')
    conf_path = os.path.join(base_dir, 'config\config.ini')
    api_env_path = base_dir + r"\report\allure\%s\%s\xml\environment.xml" % (parent_folder, child_folder)
    api_ant_report_path = base_dir + r"\report\ant\%s\%s" % (parent_folder, child_folder)
    api_report_xml_path = base_dir + r"\report\allure\%s\%s\xml" % (parent_folder, child_folder)
    generate_allure_api_report_bat = base_dir + r'\bat\generate_allure_api_report.bat'

    xml_case_path = base_dir + r"\Import\CaseXml\\"


if __name__ == "__main__":
    print(Settings.log_path, Settings.conf_path)

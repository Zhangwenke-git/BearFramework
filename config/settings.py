# -*-coding=utf8-*-
import os
from tools.TimeUtil import TimeUtils


class Settings:
    parent_folder = TimeUtils.time8
    child_folder = TimeUtils.time9

    APIcaseFileRemove = True
    APItemplateFileRemove = True
    ReportAfterClose = True
    allowTimedTask = True


    websocket_server_allowed_size = 4096

    success_flag = '通过'
    fail_flag = '失败'

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_path = os.path.join(base_dir, 'log')
    template_dir = os.path.join(base_dir,'templates')
    conf_path = os.path.join(base_dir, 'config\config.ini')
    api_env_path = base_dir + r"\report\allure\xml\environment.xml"

    api_ant_report_path = base_dir + r"\report\ant"

    api_report_xml_path = base_dir + r"\report\allure\xml"
    generate_allure_api_report_bat = base_dir + r'\bat\generate_allure_api_report.bat'

    FTP_DIR = r"C:\Users\ZWK\Desktop\FTP"

    xml_case_path = base_dir + r"\Import\CaseXml\\"


if __name__ == "__main__":
    print(Settings.log_path, Settings.conf_path)

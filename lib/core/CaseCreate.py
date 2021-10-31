# _*_coding=utf-8_*_
import json
import os
import glob
import threading
from string import Template
from config.settings import Settings

from tools.logger import Logger

logger = Logger("CaseCreation")
lock = threading.Lock()

# from data.case import data_mapping_dict


def template_json_create(data:list):
    """
    更具入参生成templates目录下的.json模板文件
    @param data:
    """
    for template_json in data:
        template_json_copy = template_json.copy()

        del template_json_copy["scenarios"]
        template_json_copy["method"]="post" if template_json_copy["method"]==1 else "get" # todo:待优化，不能写死请求方式
        template_file = os.path.join(Settings.template_dir,"test_%s.json" % template_json_copy.get("case"))
        with open(template_file,"w",encoding="utf-8") as f:
            f.write(json.dumps(template_json_copy,indent=4,ensure_ascii=False))
        f.close()


def singleFunctionCreate(caseinfo):
    """
    写入test_func测试函数，即测试用例  #todo:结果校验需要优化
    @param caseinfo:
    @return:
    """
    code = Template(r'''
    
    
    @pytest.mark.parametrize("param,desc,expect", $testdata)
    @allure.story("Case:${title}")
    @allure.severity("critical")
    def test_${testfunction}(self,param,desc,expect,json_template):
        """${description}"""
        with allure.step("step:生成测试数据"):
            case = json_template(**param)
            allure.attach(json.dumps(case,indent=4,ensure_ascii=False),"配置信息",allure.attachment_type.JSON)
        with allure.step("step:函数调用"):
            data_ = case.get('data')
            data = format_object.format_(data_)
            allure.attach(json.dumps(data,indent=4,ensure_ascii=False),"请求入参",allure.attachment_type.JSON)
        with allure.step(f"step:请求url: {case.get('url')}"):
            if case.get('method').lower()=='post':
                res = requests.post(url=case.get('url'),headers=case.get('headers'), data=data)
            else:
                res = requests.get(url=case.get('url'),headers=case.get('headers'), params=data)
        with allure.step("step:请求断言"):
            assert res.status_code == expect
        #assert json.loads(r.content)["your_input"] == return_user
''')

    string = code.substitute(testfunction=caseinfo["case"], title=caseinfo["case_title"],
                             description=caseinfo["case_description"],
                             testdata=caseinfo['scenarios'])
    return string


def singClassCreate(caseinfo):
    """
    写入测试类
    @param caseinfo:
    @return:
    """
    code = Template(r"""#-*-coding=utf8-*-
    
import pytest
import json
import requests
import allure
from lib.core.FormatParameter import FormatParam

format_object = FormatParam()

@pytest.mark.APItest
@allure.feature("Title:${class_title}")
class TestCase_${module}(object):
            """)

    string = code.substitute(module=caseinfo["module"], class_title=caseinfo["class_title"])
    return string


def create_case_class(func_map, mode='w'):
    test_case_file = os.path.join(Settings.base_dir + r'\testsuite', 'test_{}.py'.format(func_map.get("module")))
    with open(test_case_file, mode, encoding='utf-8') as f:
        f.write(singClassCreate(func_map))
    f.close()


def create_case_function(func_map, mode='a'):
    test_case_file = os.path.join(Settings.base_dir + r'\testsuite', 'test_{}.py'.format(func_map.get("module")))
    with open(test_case_file, mode, encoding='utf-8') as f:
        f.write(singleFunctionCreate(func_map))
    f.close()


def batCreate(func, _dict):
    """
    批量生成测试用例py文件
    @param func:
    @param _dict:
    """
    lock.acquire(True)
    list(map(func, _dict))
    if len(glob.glob("test_*.py")) != 0:
        lock.release()


def creation(data_mapping_dict):
    """
    生成测试用例文件的主入口
    @param data_mapping_dict:
    """
    template_json_create(data_mapping_dict)
    class_file = threading.Thread(target=batCreate, args=(create_case_class, data_mapping_dict))
    func_file = threading.Thread(target=batCreate, args=(create_case_function, data_mapping_dict))
    class_file.start()
    func_file.start()


def clear_pyfile():
    """
    清除测试用例文件
    """
    delete_files = []
    try:
        test_suit = os.path.join(Settings.base_dir,'testsuite')
        for root,dirs,files in os.walk(test_suit):
            for file in files:
                if file.startswith("test_"):
                    delete_file = os.path.join(root,file)
                    delete_files.append(delete_file)
                    os.remove(delete_file)
    except Exception:
        logger.error('Fail to remove API test case py file!')
    else:
        logger.debug(f'Success to remove API test case py file: {delete_files}')


def clear_template_file():
    """
    清除测试模板.json文件
    """
    delete_files = []
    try:
        templates = os.path.join(Settings.base_dir,'templates')
        for root,dirs,files in os.walk(templates):
            for file in files:
                if file.endswith(".json"):
                    delete_file = os.path.join(root,file)
                    delete_files.append(delete_file)
                    os.remove(delete_file)
    except Exception:
        logger.error('Fail to remove API test case py file!')
    else:
        logger.debug(f'Success to remove API test case py file: {delete_files}')

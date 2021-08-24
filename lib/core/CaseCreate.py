# _*_coding=utf-8_*_
import os
import glob
import threading
from string import Template
from config.settings import Settings

from tools.logger import Logger

logger = Logger("CaseCreation")
lock = threading.Lock()

from data.case import data_mapping_dict


def singleFunctionCreate(caseinfo):
    print(caseinfo)
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


def create_case_function(func_map, mode='a'):
    test_case_file = os.path.join(Settings.base_dir + r'\testsuite', 'test_{}.py'.format(func_map.get("module")))
    with open(test_case_file, mode, encoding='utf-8') as f:
        f.write(singleFunctionCreate(func_map))


def batCreate(func, _dict):
    lock.acquire(True)
    list(map(func, _dict))
    if len(glob.glob("test_*.py")) != 0:
        lock.release()


def creation():
    class_file = threading.Thread(target=batCreate, args=(create_case_class, data_mapping_dict))
    func_file = threading.Thread(target=batCreate, args=(create_case_function, data_mapping_dict))
    class_file.start()
    func_file.start()


def clear_pyfile():
    try:
        for item in data_mapping_dict:
            test_case_file = os.path.join(Settings.base_dir + r'\testsuite', 'test_{}.py'.format(item.get("module")))
            os.remove(test_case_file)
    except Exception:
        logger.error('Fail to remove API test case py file!')
    else:
        logger.debug('Success to remove API test case py file!')


if __name__ == '__main__':
    creation()
    # clear_pyfile()

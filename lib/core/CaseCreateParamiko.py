# coding=utf-8
import os
from string import Template

from config.settings import Settings

from tools.logger import Logger

logger = Logger("CaseCreation")

from data.case import data_mapping_dict


def singleFunctionCreate(MethodList):
    code = Template(r'''
    @pytest.mark.parametrize("json_data", $testdata,ids=[caseitem.get("scenario") for caseitem in $testdata])
    @allure.story("Case:${title}")
    @allure.severity("critical")
    def test_${testfunction}(self,json_data,json_template,record_property):
        """${description}"""
        record_property("parameter",locals())
        with allure.step("step:生成测试数据"):
            case = json_template(**json_data)
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
     
        with allure.step("step:获取响应消息关键字"):
            key_word = json.loads(res.content)[case.get('validator')]
        
        with allure.step(f"获取JSON消息"):
            processName,command,index=case.get('validator').split(":")
            json_res_list = paramikoTojson(processName, command % key_word)
            json_res = json_res_list[int(index)]


        with allure.step("读取数据库表"):
            database_dict = db_func_reflect(case.get('database'),key_word)

        with allure.step("生成对比报告"):
            report_obj = GenerateCompareReport(mapping_dict)
            dict_tuple = (data,  json_res, database_dict)
            field_result = report_obj._generateCNHtml(dict_tuple, cn_map_dic=projectFieldMapDict, black_list=None)
            html = report_obj._generateHtml(data_["scenario"], field_result, url=case.get('url'),
                                            message2=processName, message3="数据库")
            allure.attach(html, data_["scenario"], allure.attachment_type.HTML)
''')

    string = code.substitute(testfunction=MethodList["case"], title=MethodList["title"],
                             description=MethodList["description"],
                             testdata=MethodList['testdata']
                             )
    return string


def singClassCreate(MethodList):
    code = Template(r"""# coding=utf-8
    
import pytest
import json
import requests
import allure
from src.API.FormatParameter import FormatParam
from src.Utils.Compare.MappingConfig import mapping_dict
from src.API.General import paramikoTojson
from src.Utils.Compare.CN_fields_map import projectFieldMapDict
from src.Utils.Compare.CompareTemplate3 import GenerateCompareReport
from src.API.General import db_func_reflect
from src.Utils.Public.logger import Logger

format_object = FormatParam()
logger = Logger("${module}",type="API")


@pytest.mark.APItest
@allure.feature("Title:${classname}")
class TestCase_${module}(object):
            """)

    string = code.substitute(module=MethodList["module"], classname=MethodList["classname"])
    return string


def create_case_file(func_map, func_str, mode='a'):
    test_case_file = os.path.join(Settings.base_dir + '\TestSuit\API', 'test_{}.py'.format(func_map.get("module")))
    with open(test_case_file, mode, encoding='utf-8') as f:
        f.write(func_str)


def creation():
    try:
        for item in data_mapping_dict:
            create_case_file(item, singClassCreate(item), mode='w')
        for item in data_mapping_dict:
            func_str = singleFunctionCreate(item)
            create_case_file(item, func_str, mode='a')
    except Exception:
        logger.error('Fail to create API test case py file!')
    else:
        logger.debug('Success to create API test case py file!')


def clear_pyfile():
    try:
        for item in data_mapping_dict:
            test_case_file = os.path.join(Settings.base_dir + '\TestSuit\API', 'test_{}.py'.format(item.get("module")))
            os.remove(test_case_file)
    except Exception:
        logger.error('Fail to remove API test case py file!')
    else:
        logger.debug('Success to remove API test case py file!')


if __name__ == '__main__':
    creation()
    # clear_pyfile()

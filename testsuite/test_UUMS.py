#-*-coding=utf8-*-
    
import pytest
import json
import requests
import allure
from lib.core.FormatParameter import FormatParam

format_object = FormatParam()

@pytest.mark.APItest
@allure.feature("Title:UUMS用户认证系统")
class TestCase_UUMS(object):

    @pytest.mark.parametrize("param,desc,expect", [[{'name': 'ribn', 'passcode': 'aaaa1111!'}, '账号不存在密码正确', {'code': 10032, 'result': ' false', 'message': '用户不存在'}], [{'name': '猪宝宝', 'passcode': 'aaaa1111!'}, '登录账号和密码正确', {'code': 200, 'result': ' sussess'}]])
    @allure.story("Case:uums用户中心登录")
    @allure.severity("critical")
    def test_uums_login(self,param,desc,expect,json_template):
        """uums用户中心登录"""
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

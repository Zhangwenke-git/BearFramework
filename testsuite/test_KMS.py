#-*-coding=utf8-*-
    
import pytest
import json
import requests
import allure
from lib.core.FormatParameter import FormatParam

format_object = FormatParam()

@pytest.mark.APItest
@allure.feature("Title:KMS系统")
class TestCase_KMS(object):
            
    
    
    @pytest.mark.parametrize("param,desc,expect", [[{'password': ' sdad@1332', 'username': 'zhangwenke', 'remember_flag': 'true'}, '用户正确密码错误', {'code': 200}], [{'password': 'aaaa1111!', 'username': 'zhangwenke', 'remember_flag': 'true'}, '用户密码均正确', {'code': 200}]])
    @allure.story("Case:KMS用户登录接口")
    @allure.severity("critical")
    def test_login_kms(self,param,desc,expect,json_template):
        """KMS用户登录接口"""
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

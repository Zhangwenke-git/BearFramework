# -*-coding=utf8-*-
import json
import os
from functools import reduce

from config.settings import Settings


def write_template_to_json(template: dict):
    template_file = os.path.join(Settings.base_dir + r"/templates", "test_{}.json".format(template.get("case")))
    del template["scenarios"]
    if template.get("method") == 1:
        template.update({"method": "POST"})
    else:
        template.update({"method": "GET"})
    _string = json.dumps(template, indent=4, ensure_ascii=False)
    with open(template_file, "w+", encoding="utf-8") as f:
        f.write(_string)
    f.close()


def create_case_parameter(data: list):
    """
    :function:将收到的消息进行解析，解析成可以[{caseinfo1},{caseinfo2}...]
    :param data: 从前端接收到的消息体，["project":[{"suit":[caseinfo1,caseinfo2....]},{"suit":[caseinfo1,caseinfo2....]}],"project":[{"suit":[caseinfo1,caseinfo2....]},{"suit":[caseinfo1,caseinfo2....]}]...]
    :return:[{caseinfo1},{caseinfo2}...]
    """
    def merge(_dict):
        _list = []
        _list.extend(list(_dict.values())[0])
        return _list

    testsuite = list(map(merge,data))

    temp = []
    for i in testsuite:
        temp.extend(i)

    testcases = list(map(merge, temp))
    result_temp = []
    for item in testcases:
        result_temp.extend(item)

    for case in result_temp:
        scenarios_list = []
        for i in case["scenarios"]:
            scenarios_list.append(list(i.values()))
        case["scenarios"]=scenarios_list
    return result_temp


def init_data_file(api_data):
    """
    :function:生成测试模板test_xx.json文件和数据集case.py文件
    :param api_data:
    """
    res = create_case_parameter(api_data)
    _string = json.dumps(res, indent=4, ensure_ascii=False)
    case_file = os.path.join(Settings.base_dir + r"/data", "case.py")

    with open(case_file, "w+", encoding="utf-8") as f:
        content = '''# -*-coding=utf-8-*-    
null=None
false = False
true=True

data_mapping_dict =%s

        ''' % _string
        f.write(content)
    f.close()
    for i in res:
        write_template_to_json(i)


test = {'module': 'ODM', 'class_title': 'ODM交易系统', 'case': 'order_submit', 'case_title': '限价订单提交', 'case_description': None, 'templates_name': '现券XBOND订单提交', 'url': 'https://www.cnblogs.com/aaronthon/ajax/GetPostStat', 'method': 1, 'header': {'content-type': 'application/json', 'Authorization': '9480295ab2e2eddb8'}, 'data': {'ordrData': {'clntQtCd': '', 'stlmntSpdNm': 2, 'cntngncyIndctr': '', 'flxblNetPrc': '', 'qtTp': '${login}|<{{username}},{{password}}>', 'netPrc': '{{netPrc}}', 'instnCd': '{{instnCd}}', 'nmnlVol': '{{volumn}}', 'ordrTpIndctr': '1'}}, 'scenarios': [{'parameter': {'netPrc': '100.2344', 'password': 'aaaa1111!', 'instnCd': '100035', 'volumn': '1000,000', 'username': 'zhangwneke'}, 'name': '限价订单提交-T+1', 'validator': {'code': 200, 'result': ' sussess'}}]}
test2 = {'module': 'KMS', 'class_title': 'KMS系统', 'case': 'login_kms', 'case_title': 'KMS用户登录接口', 'case_description': 'KMS用户登录接口', 'templates_name': 'kms登录模板', 'url': 'http://119.123.2.1:8980/login', 'method': 1, 'header': {'Content-Type': 'application/json'},
         'data': {'id': 'ewr3-deee3-2ewq2-uhue7', 'params': {'name': '{{username}}', 'passcode': '{{password}}', ' check': '${check}|<{{remember_flag}}>}'}},
         'scenarios': [{'parameter': {'password': ' sdad@1332', 'username': 'zhangwenke', 'remember_flag': 'true'}, 'name': '用户正确密码错误', 'validator': {'code': 200}},
                       {'parameter': {'password': 'aaaa1111!', 'username': 'zhangwenke', 'remember_flag': 'true'}, 'name': '用户密码均正确', 'validator': {'code': 200}}]}

data = [{'上海证券交易所': [{'KMS': [{'module': 'KMS', 'class_title': 'KMS系统', 'case': 'login_kms', 'case_title': 'KMS用户登录接口', 'case_description': 'KMS用户登录接口', 'templates_name': 'kms登录模板', 'url': 'http://119.123.2.1:8980/login', 'method': 1, 'header': {'Content-Type': 'application/json'}, 'data': {'id': 'ewr3-deee3-2ewq2-uhue7', 'params': {'name': '{{username}}', 'passcode': '{{password}}', 'check': '${check}|<{{remember_flag}}>'}}, 'scenarios': [{'parameter': {'password': ' sdad@1332', 'username': 'zhangwenke', 'remember_flag': 'true'}, 'name': '用户正确密码错误', 'validator': {'code': 200}}, {'parameter': {'password': 'aaaa1111!', 'username': 'zhangwenke', 'remember_flag': 'true'}, 'name': '用户密码均正确', 'validator': {'code': 200}}]}]}]}, {'中国外汇交易中心项目': [{'ODM': [
{'module': 'ODM', 'class_title': 'ODM交易系统', 'case': 'order_submit', 'case_title': '限价订单提交', 'case_description': None, 'templates_name': '现券XBOND订单提交', 'url': 'https://www.cnblogs.com/aaronthon/ajax/GetPostStat', 'method': 1, 'header': {'content-type': 'application/json', 'Authorization': '9480295ab2e2eddb8'}, 'data': {'ordrData': {'clntQtCd': '', 'stlmntSpdNm': 2, 'cntngncyIndctr': '', 'flxblNetPrc': '', 'qtTp': '${login}|<{{username}},{{password}}>', 'netPrc': '{{netPrc}}', 'instnCd': '{{instnCd}}', 'nmnlVol': '{{volumn}}', 'ordrTpIndctr': '1'}}, 'scenarios': [{'parameter': {'netPrc': '100.2344', 'password': 'aaaa1111!', 'instnCd': '100035', 'volumn': '1000,000', 'username': 'zhangwneke'}, 'name': '限价订单提交-T+1', 'validator': {'code': 200, 'result': ' sussess'}}]}]}]}]


data = [{'上海证券交易所': [{'UUMS': [{'module': 'UUMS', 'class_title': 'UUMS用户认证系统', 'case': 'uums_login', 'case_title': 'uums用户中心登录', 'case_description': 'uums用户中心登录', 'templates_name': 'uums用户中心登录模板', 'url': 'https://www.sojson.com/','method': 1, 'header': {'Content-Type': 'application/json'}, 'data': {'username': '{{name}}', 'passcode': '{{passcode}}'}, 'scenarios': [{'parameter': {'name': 'ribn', 'passcode': 'aaaa1111!'}, 'name': '账号不存在密码正确', 'validator': {'code': 10032, 'result': ' false', 'message': '用户不存在'}}, {'parameter': {'name': '猪宝宝', 'passcode': 'aaaa1111!'}, 'name': '登录账号和密码正确', 'validator': {'code': 200, 'result': ' sussess'}}]}]},
                     {'KMS': [{'module':'KMS', 'class_title': 'KMS系统', 'case': 'login_kms', 'case_title': 'KMS用户登录接口', 'case_description': 'KMS用户登录接口', 'templates_name': 'kms登录模板', 'url': 'http://119.123.2.1:8980/login', 'method': 1, 'header': {'Content-Type': 'application/json'}, 'data': {'id': 'ewr3-deee3-2ewq2-uhue7', 'params': {'name': '{{username}}', 'passcode': '{{password}}', 'check': '${check}|<{{remember_flag}}>'}}, 'scenarios': [{'parameter': {'password': ' sdad@1332', 'username': 'zhangwenke', 'remember_flag': 'true'}, 'name': '用户正确密码错误', 'validator': {'code': 200}}, {'parameter': {'password': 'aaaa1111!', 'username': 'zhangwenke', 'remember_flag': 'true'}, 'name': '用户密码均正确', 'validator': {'code': 200}}]}]}]}, {'中国外汇交易中心项目': [{'ODM': [{'module': 'ODM', 'class_title': 'ODM交易系统', 'case': 'order_submit', 'case_title': '限价订单提交', 'case_description': None, 'templates_name': '现券XBOND订单提交', 'url': 'https://www.cnblogs.com/aaronthon/ajax/GetPostStat', 'method': 1, 'header': {'content-type': 'application/json', 'Authorization': '9480295ab2e2eddb8'
}, 'data': {'ordrData': {'clntQtCd': '', 'stlmntSpdNm': 2, 'cntngncyIndctr': '', 'flxblNetPrc': '', 'qtTp': '${login}|<{{username}},{{password}}>', 'netPrc': '{{netPrc}}', 'instnCd': '{{instnCd}}', 'nmnlVol': '{{volumn}}', 'ordrTpIndctr': '1'}}, 'scenarios': [{'parameter': {'netPrc': '100.2344', 'password': 'aaaa1111!', 'instnCd': '100035', 'volumn': '1000,000', 'username': 'zhangwneke'}, 'name': '限价订单提交-T+1', 'validator': {'code': 200, 'result': ' sussess'}}]}]}]}]

if __name__ == "__main__":
    # res = create_case_parameter(data)
    # print(res)
    # for i in res:
    #     write_template_to_json(i)

    init_data_file(data)



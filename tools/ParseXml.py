# -*- coding:utf-8 -*-


import json
from xml.dom import minidom
from config.settings import Settings
from tools.DataUtil import DataUtil


class PraseXml(object):

    def writeXML(self, cases: list, xml_name):
        """
        :将API接口测试用例生成XML文件
        :param cases: list type
        :param xml_name: xml名称
        """
        imp = minidom.getDOMImplementation()
        xml_file = Settings.xml_case_path + xml_name + '.xml'
        # 建立根节点
        domTree = imp.createDocument(None, 'collection', None)

        rootNode = domTree.documentElement

        for case in cases:
            # 新建一个case节点
            case_node = domTree.createElement("case")
            # 给节点添加属性ID，且格式为0001,0002,0003...
            case_node.setAttribute("ID", str(cases.index(case)).zfill(4))

            # 创建key节点,并设置value
            for key in sorted(case.keys()):
                value = case.get(key)
                if key == "detail" and not value.startswith("<![CDATA["):
                    value = "<![cdata[{}]]>".format(value)

                node = domTree.createElement(key)
                if isinstance(value, (str, int, float, bytes, bool)):
                    # 通过__name__获取<class 'str'>的名字:str
                    node.setAttribute("type", type(value).__name__)
                    value = str(value)
                elif isinstance(value, (dict, list)):
                    node.setAttribute("type", type(value).__name__)
                    value = json.dumps(value, ensure_ascii=False)  # ensure_ascii=False解决中文乱码的问题

                text_value = domTree.createTextNode(value)
                node.appendChild(text_value)  # 把文本节点挂到key节点
                case_node.appendChild(node)

            # 创建comments节点,这里是CDATA
            comments_node = domTree.createElement("comments")
            cdata_text_value = domTree.createCDATASection("This is a remark,comments or description!")
            comments_node.appendChild(cdata_text_value)
            case_node.appendChild(comments_node)

            rootNode.appendChild(case_node)

        with open(xml_file, 'w', encoding='utf-8') as f:
            domTree.writexml(f, addindent='  ', encoding='utf-8')

    def readXML(self, xml_path):
        domTree = minidom.parse(xml_path)
        # 文档根元素
        rootNode = domTree.documentElement

        # 所有根节点CASE
        cases = rootNode.getElementsByTagName("case")

        case_list = []
        for case in cases:
            if case.hasAttribute("ID"):

                # data 元素
                case_child = case.childNodes
                # 获取子元素的tag名称
                tag_list = [child.nodeName for child in case_child]
                # 对tag名称去重
                tag_list = [tag for tag in tag_list if tag != '#text']

                dict_ = {}
                for tagNm in tag_list:
                    key = case.getElementsByTagName(tagNm)[0]
                    value = key.childNodes[0].data
                    datatype = key.getAttribute("type")
                    if datatype in ["dict", "list"]:
                        value = json.loads(value, encoding='utf-8')
                    elif datatype == "int":
                        value = int(value)
                    elif datatype == "float":
                        value = float(value)
                    elif datatype == "bool":
                        value = eval(value)
                    elif datatype == "bytes":
                        value = bytes(value)
                    else:
                        value = str(value)
                    dict_[tagNm] = value

                case_list.append(dict_)
            return case_list

    def writeStepsXml(self, cases: list, xml_name):
        imp = minidom.getDOMImplementation()
        xml_file = Settings.xml_case_path + xml_name + '.xml'
        domTree = imp.createDocument(None, 'collection', None)

        rootNode = domTree.documentElement

        for case in cases:
            # 新建一个case节点
            case_node = domTree.createElement("scenario")
            case_node.setAttribute("scenario_id", str(cases.index(case) + 1).zfill(4))

            # 创建key节点,并设置value
            for key in sorted(case.keys()):
                value = case.get(key)
                if key == "detail" and not value.startswith("<![CDATA["):
                    value = "<![cdata[{}]]>".format(value)

                node = domTree.createElement(key)
                if key == "steps":
                    for step in case.get("steps"):
                        step_node = domTree.createElement("step")
                        step_node.setAttribute("step_id", str(case.get("steps").index(step) + 1).zfill(4))
                        dict_value = json.dumps(step, ensure_ascii=False)
                        step_value = domTree.createTextNode(dict_value)
                        step_node.appendChild(step_value)
                        node.appendChild(step_node)

                else:
                    if isinstance(value, (str, int, float, bytes, bool)):
                        node.setAttribute("type", type(value).__name__)
                        value = str(value)
                    elif isinstance(value, (dict, list)):
                        node.setAttribute("type", type(value).__name__)
                        value = json.dumps(value, ensure_ascii=False)
                    text_value = domTree.createTextNode(value)
                    node.appendChild(text_value)  # 把文本节点挂到name_node节点
                case_node.appendChild(node)

            # 创建comments节点,这里是CDATA
            comments_node = domTree.createElement("comments")
            cdata_text_value = domTree.createCDATASection("A small but healthy company.")
            comments_node.appendChild(cdata_text_value)
            case_node.appendChild(comments_node)
            rootNode.appendChild(case_node)

        with open(xml_file, 'w', encoding='utf-8') as f:
            # domTree.writexml(f, addindent='  ', encoding='utf-8')  # 压缩输出
            domTree.writexml(f, addindent='\t', newl='\n', encoding='utf-8')  # 格式化输出

    def readJunitXML(self, xml_path):
        domTree = minidom.parse(xml_path + r"\junitXml.xml")
        testsuites = domTree.documentElement
        testsuite = testsuites.getElementsByTagName("testsuite")[0]

        xml_dict = {}

        start = testsuite.getAttribute("timestamp")
        durations = testsuite.getAttribute("time")
        total = testsuite.getAttribute("tests")
        errors = testsuite.getAttribute("errors")
        failed = testsuite.getAttribute("failures")
        skipped = testsuite.getAttribute("skipped")

        passed = int(total) - int(failed) - int(skipped) - int(errors)

        xml_dict["pyfile"] = "wwww.zwk.com.cn"
        xml_dict["start"] = start
        xml_dict["durations"] = durations
        xml_dict["total"] = total
        xml_dict["failed"] = failed
        xml_dict["skipped"] = skipped
        xml_dict["passed"] = passed
        xml_dict["errors"] = errors

        environment_properties = testsuite.getElementsByTagName("properties")[0]
        environments = environment_properties.getElementsByTagName("property")

        environment_dict = {environment_.getAttribute("name"): environment_.getAttribute("value") for environment_ in
                            environments}
        xml_dict["environment"] = environment_dict

        case_list = []
        testcases = testsuite.getElementsByTagName("testcase")

        for testcase in testcases:
            case_dict = dict()
            case_dict["scenario"] = testcase.getAttribute("classname")
            case_dict["name"] = testcase.getAttribute("name").encode('utf-8').decode('unicode_escape')  # 将用例名称转换成中文
            case_dict["duration"] = testcase.getAttribute("time")
            case_dict["times"] = 1

            failure_list = testcase.getElementsByTagName("failure")
            error_list = testcase.getElementsByTagName("error")
            skip_list = testcase.getElementsByTagName("skipped")

            if len(failure_list) != 0:
                errors = failure_list[0].getAttribute("message")
                detail = failure_list[0].childNodes[0].data
                outcome = "Failed"

            elif len(skip_list) != 0:
                outcome = "Skipped"
                errors = skip_list[0].getAttribute("message")
                detail = skip_list[0].childNodes[0].data

            elif len(error_list) != 0:
                outcome = "Error"
                errors = error_list[0].getAttribute("message")
                detail = error_list[0].childNodes[0].data
            else:
                errors = ""
                detail = ""
                outcome = "Passed"

            case_dict["errors"] = errors
            case_dict["outcome"] = outcome
            case_dict["detail"] = detail

            properties = testcase.getElementsByTagName("properties")
            if len(properties) != 0:
                parameters = properties[0]
                parameters_ = parameters.getElementsByTagName("property")
                parameter_dict = {parameter.getAttribute("name"): parameter.getAttribute("value") for parameter in
                                  parameters_}
                case_dict["parameter"] = parameter_dict

            system_err = testcase.getElementsByTagName("system-err")
            if len(system_err) != 0:
                log = system_err[0].childNodes[0].data
                case_dict["log"] = log

            case_list.append(case_dict)

        scenario_name_list = [case.get("scenario") for case in case_list]
        duraions_list = [float(case.get("duration")) for case in case_list]

        scenario_name_list = DataUtil().listNoRepeat(scenario_name_list)
        scenario_list = []
        for scenario_name in scenario_name_list:
            scenario_cases = []
            scenario_dict = dict()
            for case in case_list:
                try:
                    if scenario_name == case["scenario"]:
                        del case["scenario"]
                        scenario_cases.append(case)
                    scenario_dict["cases"] = scenario_cases
                    scenario_dict["scenario"] = scenario_name
                except KeyError:
                    pass
            scenario_list.append(scenario_dict)

        xml_dict["data"] = scenario_list
        xml_dict["minimum"] = min(duraions_list)
        xml_dict["maximum"] = max(duraions_list)

        return xml_dict


if __name__ == '__main__':
    sample = PraseXml()
    from data.case import data_mapping_dict

    case_ = [{'module': 32.2101, 'case': 11, 'classname': True, 'title': {"key1": 200, "key2": "TT"},
              'description': '现券XBOND限价订单提交', 'testdata': [
            {'scenario': '主代从-买入-不分仓-T+1', 'instnCd': 100035, 'trdngAcntCd': '100035', 'traTlCd': 180210,
             'bndsNm': '债券180210', 'dir': True, 'netPrc': 105, 'instnNm': '中信证券', 'trdrCd': '6274', 'volumn': 100000000,
             'validator': {"key1": 200, "key2": "TT"},
             'prcoess': "TBS-DP-CSS:grep '%s' /home/tbs/app/tbs-dp-css/logs/css-debug.log:0", 'database': '订单信息表'},
            {'scenario': '限价订单-卖出-不分仓-T+0', 'instnCd': '100035', 'trdngAcntCd': '100035', 'traTlCd': '140210',
             'bndsNm': '债券140210', 'dir': 'S', 'netPrc': '102', 'instnNm': '中信证券', 'trdrCd': '6270',
             'volumn': '200000000', 'validator': 'ordrCd',
             'prcoess': "TBS-DP-CSS:grep '%s' /home/tbs/app/tbs-dp-css/logs/css-debug.log:1", 'database': '订单信息表'},
            {'scenario': '弹性订单-买入-不分仓-T+0', 'instnCd': '401352', 'trdngAcntCd': '401352', 'traTlCd': '170020',
             'bndsNm': '债券170020', 'dir': 'B', 'netPrc': '100', 'instnNm': '阳光资管', 'trdrCd': '30086',
             'volumn': '50000000', 'validator': 'ordrCd',
             'prcoess': "TBS-DP-CSS:grep '%s' /home/tbs/app/tbs-dp-css/logs/css-debug.log:2", 'database': '订单信息表'},
            {'scenario': '限价订单-买入-分仓-T+1', 'instnCd': '100003', 'trdngAcntCd': 100003, 'traTlCd': 170011,
             'bndsNm': '债券170011', 'dir': 'B', 'netPrc': 100, 'instnNm': '农业银行', 'trdrCd': 'yedan',
             'volumn': '80000000', 'validator': 'ordrCd',
             'prcoess': "TBS-DP-CSS:grep '%s' /home/tbs/app/tbs-dp-css/logs/css-debug.log:3", 'database': '订单信息表'}]},
             {'module': 'XSWAP_PARAMIKO_CBT', 'case': 'irs_paramiko_cbt', 'classname': '衍生品订单提交', 'title': '限价订单',
              'description': '衍生品利率互换实时承接限价订单提交', 'testdata': [
                 {'scenario': '主代从-买入-不分仓-T+1', 'instnCd': '100035', 'trdngAcntCd': '100035', 'contract': 'FR007_1Y',
                  'contractNm': 'FR007_1Y', 'dir': 'B', 'price': '105.221', 'instnNm': '中信证券', 'trdCd': '6274',
                  'volumn': '100000000', 'validator': '200'},
                 {'scenario': '限价订单-卖出-不分仓-T+0', 'instnCd': '100035', 'trdngAcntCd': '100035', 'contract': 'FR007_2Y',
                  'contractNm': 'FR007_2Y', 'dir': 'S', 'price': '105.222', 'instnNm': '中信证券', 'trdCd': '6270',
                  'volumn': '200000000', 'validator': '200'},
                 {'scenario': '弹性订单-买入-不分仓-T+0', 'instnCd': '401352', 'trdngAcntCd': '401352', 'contract': 'FR007_3Y',
                  'contractNm': 'FR007_3Y', 'dir': 'B', 'price': '105.223', 'instnNm': '阳光资管', 'trdCd': '30086',
                  'volumn': '50000000', 'validator': '200'},
                 {'scenario': '限价订单-买入-分仓-T+1', 'instnCd': '100003', 'trdngAcntCd': '100003', 'contract': 'FR007_4Y',
                  'contractNm': 'FR007_4Y', 'dir': 'B', 'price': '105.224', 'instnNm': '农业银行', 'trdCd': 'yedan',
                  'volumn': '80000000', 'validator': '200'}]}]

    step_ = [
        {
            "scenario": "登录",
            "steps": [
                {
                    "title": "username",
                    "description": "用户名",
                    "method": "xpath",
                    "value": "//input[@id='user']",
                },
                {
                    "title": "password",
                    "description": "密码",
                    "method": "classname",
                    "value": "pwd",
                },
                {
                    "title": "phone",
                    "description": "密码",
                    "method": "classname",
                    "value": "pwd",
                }, {
                    "title": "site",
                    "description": "密码",
                    "method": "classname",
                    "value": "pwd",
                }
            ]
        },
        {
            "scenario": "我要报价",
            "steps": [
                {
                    "title": "username",
                    "description": "用户名",
                    "method": "xpath",
                    "value": "//input[@id='user']",
                },
                {
                    "title": "password",
                    "description": "密码",
                    "method": "classname",
                    "value": "pwd",
                }
            ]
        },
        {
            "scenario": "我的订单",
            "steps": [
                {
                    "title": "username",
                    "description": "用户名",
                    "method": "xpath",
                    "value": "//input[@id='user']",
                },
                {
                    "title": "password",
                    "description": "密码",
                    "method": "classname",
                    "value": "pwd",
                }
            ]
        },
        {
            "scenario": "订单查询",
            "steps": [
                {
                    "title": "username",
                    "description": "用户名",
                    "method": "xpath",
                    "value": "//input[@id='user']",
                },
                {
                    "title": "password",
                    "description": "密码",
                    "method": "classname",
                    "value": "pwd",
                }
            ]
        },
        {
            "scenario": "成交查询",
            "steps": [
                {
                    "title": "username",
                    "description": "用户名",
                    "method": "xpath",
                    "value": "//input[@id='user']",
                },
                {
                    "title": "password",
                    "description": "密码",
                    "method": "classname",
                    "value": "pwd",
                }
            ]
        },
    ]

    # sample.writeXML(case_, 'submitOrder')

    # sample2 = ReadExcle(CFETS_page_obj_element)
    # scenario_list = sample2.get_all_steps()
    # sample.writeStepsXml(scenario_list, 'submitOrderSteps')
    # xml_case = xml_case_path + '/submitOrder.xml'

    # print(sample.readXML(xml_case))
    data_xml = r'C:\Users\ZWK\Desktop\AutomaticFramework\report\ant\WEB\20201225\202012252152'

    print(sample.readJunitXML(data_xml))

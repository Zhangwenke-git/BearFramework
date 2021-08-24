# -*-coding=utf-8-*-

from tools import RegExpUtil
from tools.linuxParamiko import MyParamiko
from tools.logger import Logger

logger = Logger("paramikoTojson")
globals = {
    "true": True,
    "null": None,
    "false": False
}


def paramikoTojson(processNm, command, pattern=r'\{.*\S\}'):
    """
    :function:通过正则匹配查出字符串中的dict类型数据并返回一个List
    :param processNm: 进行名称
    :param command: 'grep key_word GateWay.log'
    :param pattern: 正则表达式
    :return: [dict1,dict2,dict3....]
    """
    logger.debug(f'Prepare to execute command: {command} in precess: {processNm}')
    dict_list = []
    try:
        paramiko_ibj = MyParamiko(processNm)
        result = paramiko_ibj.run_cmd(command)
        re = RegExpUtil.RegExpUtil()
        alist = re.findAll(string=result, pattern=pattern, mult_flag=True)[0].split("\n")
        logger.debug(f"Success to find {len(alist)} in total!")
        dict_list = []
        for item in alist:
            dict_list.append(eval(re.findAll(item, pattern=pattern)[0], globals))  # eval(exprssion,locals,globals)去掉双引号
    except Exception as e:
        logger.error(f'Fail to execute command,error as follows:{e}!')
    finally:
        return dict_list


def db_func_reflect(funcNm, key_word):
    """
    :function:根据函数名称在数据中找到对应的函数，并传入参数key_word，并执行返回结果
    :param funcNm:
    :param key_word:
    :return:
    """
    from data.api_case_mapping.FunctionMapping import function_mapping
    from tools.FormatFunc import executeStringFunc
    from src.Senarios.API.XBOND import APIdb
    function_name = function_mapping.get(funcNm)

    api_db_obj = APIdb()
    return executeStringFunc(api_db_obj, function_name, key_word)

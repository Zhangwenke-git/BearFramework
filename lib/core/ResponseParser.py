from tools.logger import Logger

logger = Logger("parser_response")


def parser_response(expression: str, dict_: dict):
    try:
        suer = expression.split(".")
        if suer[0] != 0 and isinstance(dict_, dict):
            if suer[0] in dict_.keys():
                value = dict_[suer[0]]
                if isinstance(value, dict):
                    del (suer[0])
                    usr = ".".join(suer)
                    value = parser_response(usr, value)
                elif isinstance(value, list):
                    del (suer[0])
                    usr = ".".join(suer)
                    try:
                        index = int(usr[0])
                    except TypeError:
                        pass
                    else:
                        del (suer[0])
                        usr = ".".join(suer)
                        try:
                            value = value[index]
                        except IndexError:
                            value = "索引过长"
                        value = parser_response(usr, value)
                else:
                    if len(suer) > 1:
                        value = "表达式%s过长" % expression
                    else:
                        value = str(value)
            else:
                value = "%s不在%s之中" % (suer[0], dict_)
        elif isinstance(dict_, list):
            try:
                index = int(expression[0])
            except TypeError:
                pass
            else:
                del (suer[0])
                usr = ".".join(suer)
                try:
                    value = dict_[index]
                except IndexError:
                    value = "索引过长"
                value = parser_response(usr, value)
        else:
            value = str(dict_)
    except Exception:
        value = "未知异常，请检查表达式"
    finally:
        return value


if __name__ == "__main__":
    dict_ = {
        "success":False,
        "result":[
            {
                "name":"zek",
                "age":12
            },
            {
                "name": "wek",
                "age": 13
            },
            ["14","15"]
        ],
        "info":{
            "site":"Shanghai",
            "code":100234
        }
    }
    expression = "result.2.1"
    print(parser_response(expression,dict_))
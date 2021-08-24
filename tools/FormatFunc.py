from operator import methodcaller
from tools.logger import Logger

logger = Logger("FormatFunction")

def getClassFuncNm(objectName):
    """
    :function:获取一个类下所有的函数名称
    :param objectName:class的名称
    :return:
    """
    try:
        function_name_list = list(
            filter(lambda m: not m.startswith("__") and not m.endswith("__") and callable(getattr(objectName, m)),
                   dir(objectName)))
    except Exception as e:
        logger.error(f'Fail to get the function name list below class object: {objectName}')
    else:
        return function_name_list


def executeStringFunc(object,funcName,*args,**kwargs):
    if hasattr(object,funcName):
        try:
            result = getattr(object,funcName)(*args,**kwargs)
        except Exception as e:
            logger.error(f"Fail to execute function: {funcName}, error as follow: {e}!")
        else:
            return result
    else:
        logger.error(f"The class object does not have the function :{funcName}")



def callStringFunc(object,funcName,*args,**kwargs):
    if hasattr(object,funcName):
        try:
            result = methodcaller(funcName,*args,**kwargs)(object)
        except Exception as e:
            logger.error(f"Fail to execute function: {funcName}, error as follow: {e}!")
        else:
            return result
    else:
        logger.error(f"The class object does not have the function :{funcName}")


def executeStaticFunc(objectName,staticFuncName,*args,**kwargs):
    if hasattr(objectName,staticFuncName):
        try:
            result = getattr(objectName,staticFuncName)(*args,**kwargs)
        except Exception as e:
            logger.error(f"Fail to execute function: {staticFuncName}, error as follow: {e}!")
        else:
            return result
    else:
        logger.error(f"The class object does not have the static function :{staticFuncName}")





data = [{"add":[1,2]},{"rem":[6,2]}]



if __name__ == "__main__":
    from lib.busyness.BaseFunSet import BasePage

    print(getClassFuncNm(BasePage))

    class Test():
        def add(self,a,b):
            return a+b
        def rem(self,c,d):
            return c-d
        @staticmethod
        def cf(e,f):
            return e*f

    print(getClassFuncNm(Test))
    test_obj = Test()
    print(executeStringFunc(test_obj,'add',12,3,))
    print(callStringFunc(test_obj,'rem',12,3,))
    print(executeStaticFunc(Test,'cf',12,3,))
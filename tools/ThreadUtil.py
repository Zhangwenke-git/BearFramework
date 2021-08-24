from concurrent.futures import ThreadPoolExecutor

def multiProcess(function,param_list):
    try:
        length = len(param_list)
        nums = 4
        if length < nums:
            if length == 0:
                return "The parameter list is blank!"
            else:
                n = length
        else:
            n=nums

        with ThreadPoolExecutor(n) as executor:
            executor.map(function,param_list)
    except Exception as e:
        print("Fail to execute, error as follow: {e}!")
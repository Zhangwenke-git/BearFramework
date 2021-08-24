import os
import subprocess
from tools import logger

logger = logger.Logger("DosCmdUtils")


class DosCmd(object):
    '''
    用来封装windows执行dos命令，分两种，一种是收集执行结果，一种是不需要收集执行结果
    '''

    def excute_cmd_result(self, command):
        '''
        执行command命令，并返回执行结果
        :param command: 传入要执行的命令，字符串格式
        :return:返回执行结果，列表格式
        '''
        result_list = []
        result = os.popen(command).readlines()
        for i in result:
            if i == '\n':
                continue
            result_list.append(i.strip('\n'))  # strip() 方法用于移除字符串头尾指定的字符
        return result_list

    def excute_bat(self, batfile):
        """
        :function:执行批处理文件
        :param batfile: .bat路径
        """
        logger.debug(f'Prepare to execute bat file : {batfile}')
        popen_obj = subprocess.Popen(batfile, shell=True, stdout=subprocess.PIPE)
        stdout, stderr = popen_obj.communicate()
        if popen_obj.returncode == 0:
            logger.debug(f'Success to execute bat file!')
        else:
            logger.error(f'Fail to execute bat file!')

    def excute_cmd(self, command):
        '''
        仅执行command命令，不收集执行结果
        :param command: 传入要执行的命令，字符串格式
        '''
        os.system(command)


if __name__ == "__main__":
    dos = DosCmd()
    # print(dos.excute_cmd_result('adb devices'))
    # dos.excute_cmd('adb devices')

    from S.path_config import clear_log_bat, base_dir, generate_allure_report_bat

    # os.environ['PATH'] += os.pathsep + base_dir
    print(os.environ['PATH'])
    print(clear_log_bat)
    dos.excute_bat(clear_log_bat)
    dos.excute_bat(generate_allure_report_bat)

import json
import os
from tools import logger

logger = logger.Logger("FileUtils")


class FileUtils(object):

    def getFileNameList(self, dirpath):
        """
        :function:获取一个文件下所有的文件名称，并以一个list返回
        :param path:文件夹下的路径
        :return:list中包含文件夹和文件
        """
        logger.debug(f"Preapre to get filename under path [{dirpath}]")
        return os.listdir(dirpath)

    def judgeFileDownload(self, dirpath, filename):
        """
        :function:判断一个文件是否在某个文件夹下存在
        :param dirpath: 文件夹的路径
        :param filename: 文件名，不是文件的路径
        :return:
        """
        flag = False
        if self.judgeFileExist(dirpath):
            if filename in self.getFileNameList(dirpath):
                flag = True
                logger.debug(f'The file: {filename} exists!')
            else:
                logger.error(f'File: {filename} does not exist!')
        return flag

    def judgeFileExist(self, path):
        """
        :function：判断文件或者文件夹是否存在
        :param path:
        :return:
        """
        flag = False
        if os.path.exists(path):
            flag = True
            logger.debug(f'File: {path} exists!')
        else:
            logger.error(f'File: {path} does not exist!')
        return flag

    def getFileSize(self, path):
        """
        :function：判断文件大小
        :param path:
        :return:
        """
        size = None
        if self.judgeFileExist(path):
            size = os.path.getsize(path)
            if size == 0:
                logger.debug(f'The file: {path} is empty!')
            else:
                logger.debug(f'The size of file: {path} is :{size}!')
        return size

    def getFileCount(self, dirpath):
        """
        :function:获取一个文件夹下文件的个数，因为有的时候下载的文件重名，就会显示为：filename.format(1),这样的情况使用judgeFileDownload不行，只能通过下载文件前后，判断文件夹下的文件的数量是否有增长
        :param dirpath:
        :return:
        """
        count = None
        if self.judgeFileExist(dirpath):
            count = int(len([lists for lists in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, lists))]))
        logger.debug(f'The count of files is: {count}!')
        return count

    def getDirCount(self, dirpath):
        """
        :function:获取一个文件夹下文件夹的个数
        :param dirpath:
        :return:
        """
        count = None
        if self.judgeFileExist(dirpath):
            count = int(len([lists for lists in os.listdir(dirpath) if os.path.isdir(os.path.join(dirpath, lists))]))
        logger.debug(f'The count of dirs is: {count}!')
        return count

    def createFile(self,filepath):
        """
        :function:文件不存在就创建一个，但其所在的文件夹必须存在，如果不存在，可以使用createFolder
        :param filepath:
        """
        with open(filepath,mode='a',encoding='utf-8') as f:
            f.close()

    def createFolder(self,folder):
        """
        :function:文件夹不存在就创建一个
        :param filepath:
        """
        if not os.path.exists(folder):
            os.makedirs(folder)

    def createBatFile(self,bat_string,bat_path):
        """
        :function:生成一个bat文件
        :param bat_string: 文件字符串
        :param bat_path: 生成的路径
        """
        file_obj = open(bat_path, "w")
        try:
            file_obj.write(bat_string)
        except Exception:
            logger.error(f'Fail to create bat file : {bat_path}')
        else:
            logger.debug(f'Success to create bat file : {bat_path}')
        finally:
            file_obj.close()








if __name__ == '__main__':
    obj = FileUtils()
    # file = r'C:\Users\zwk\Desktop\V147-API\反馈和通知消息推送.xlsx'
    # dir = r'C:\Users\zwk\Desktop\V147-API'
    # filename = 'xrepo-API命令20200507.xlsx'
    # print(obj.judgeFileExist(file))
    # print(obj.getFileCount(dir))
    # print(obj.getFileNameList(dir))
    # print(obj.getDirCount(dir))
    #
    # print(obj.getFileSize(file))
    # print(obj.judgeFileDownload(dir, filename))
    file = r'C:\Users\ZWK\Desktop\rr.txt'
    obj.createFile(file)

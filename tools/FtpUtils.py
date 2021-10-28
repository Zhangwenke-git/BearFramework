from ftplib import FTP
from tools.logger import Logger
from tools.ReadConfig import ReadConfig
logger = Logger("FTP")

class FTPHelper(object):

    def __init__(self,ip,username,password,port=21,bufsize=1024,obj=None):
        self.ip=ip
        self.username=username
        self.password=password
        self.port = port
        self.bufsize=bufsize
        self.obj=obj

        ftp = FTP()  # 设置变量
        ftp.set_debuglevel(2)  # 打开调试级别2，显示详细信息
        ftp.connect(self.ip,self.port)  # 连接的ftp sever和端口
        try:
            ftp.login(self.username,self.password)  # 连接的用户名，密码
        except Exception as e:
            logger.error(f"Fail to login [{self.ip,self.port}] with user info [{self.username,self.password}]")
        else:
            logger.info(ftp.getwelcome())
            self.obj =ftp

    def cmd_dir(self,path):
        self.obj.cwd(path)  # 进入远程目录

    def close(self):
        self.obj.quit()




    # filename = "filename.txt"  # 需要下载的文件
    # file_handle = open(filename, "wb").write  # 以写模式在本地打开文件
    # ftp.retrbinaly("RETR filename.txt", file_handle, bufsize)  # 接收服务器上文件并写入本地文件
    # ftp.set_debuglevel(0)  # 关闭调试模式
    # ftp.quit()  # 退出ftp
    #
    # ftp相关命令操作
    # ftp.cwd(pathname)  # 设置FTP当前操作的路径
    # ftp.dir()  # 显示目录下所有目录信息
    # ftp.nlst()  # 获取目录下的文件
    # ftp.mkd(pathname)  # 新建远程目录
    # ftp.pwd()  # 返回当前所在位置
    # ftp.rmd(dirname)  # 删除远程目录
    # ftp.delete(filename)  # 删除远程文件
    # ftp.rename(fromname, toname)  # 将fromname修改名称为toname。
    # ftp.storbinaly("STOR filename.txt", file_handel, bufsize)  # 上传目标文件
    # ftp.retrbinary("RETR filename.txt", file_handel, bufsize)  # 下载FTP文件


if __name__ == "__main__":
    ip,port,user,pwd = ReadConfig.getFtp()
    ftp = FTPHelper(ip=ip,password=pwd,port=port,username=user)
    ftp.cmd_dir(r"/report")
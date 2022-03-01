#coding=utf-8

__description__ = """
    start an socket server ,and will wait for a client to connect,the execute pytest main function,and will generate a
    report with a way of html file! The html file will be upload to Ftp server,and then return an ftp dirs path.The client
    will download the report according to the received dirs path to a temp report,and then with the method of loading frame,
    the content of html file will be displayed on web!
"""

import json
import os
import socket
import datetime
from threading import Thread
from tools.FtpUtils import FTPHelper
from tools.logger import Logger
from tools.ReadConfig import ReadConfig
from config.settings import Settings
from testsuite.runner import yield_pytest_exe


logger = Logger("Socket server")

class SocketServer():
    def __init__(self):
        self.server= None
        self.client_pools = []

    def pre_process(self):
        if Settings.APIcaseFileRemove:
            from lib.core.CaseCreate import clear_pyfile
            clear_pyfile()

        if Settings.APItemplateFileRemove:
            from lib.core.CaseCreate import clear_template_file
            clear_template_file()


    def initializer(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind(ReadConfig.getWebsocket())
            self.server.listen(5)
        except Exception as e:
            logger.error(f"Fail to start socket server with info [{ReadConfig.getWebsocket()}],error as follows:{str(e)}")
        else:
            logger.info(f"Socket server [{ReadConfig.getWebsocket()}] is running.....")


    def accept_client(self):
        while True:
            client, addr = self.server.accept()  # 阻塞，等待客户端连接
            logger.info(
                '********************************************Client: %s has connected at %s ********************************************' % ((addr,), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            # 加入连接池
            self.client_pools.append(client)
            # 给每个客户端创建一个独立的线程进行管理
            t = Thread(target=self.handler, args=(client,))
            # 设置成守护线程
            t.daemon=True
            t.start()


    def handler(self,client):
        #client.sendall("连接服务器成功!".encode(encoding='utf8'))
        while True:
            data = client.recv(Settings.websocket_server_allowed_size)
            data = data.decode(encoding="utf-8")
            logger.debug(f"Server received data is:{data}")

            data = json.loads(data)
            if len(data) == 0:
                client.close()
                # 删除连接
                self.client_pools.remove(client)
                print("有一个客户端下线了。")
                break
            elif data == "terminate":
                pass
            else:
                start = datetime.datetime.now()
                logger.info(f"Start to execute work at {start.strftime('%Y-%m-%d %H:%M:%S')}")

                pytest_obj = yield_pytest_exe().__next__()
                flag,summary = pytest_obj.execute(data)

                end = datetime.datetime.now()
                logger.info(
                    f"The execution ends at {end.strftime('%Y-%m-%d %H:%M:%S')},and duration is {(end - start).seconds}")

                dirs = ""
                if flag:
                    _date = datetime.datetime.now().strftime("%Y%m%d")
                    _time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

                    for root, dirs, files in os.walk(Settings.api_ant_report_path):
                        ip, port, user, pwd = ReadConfig.getFtp()
                        ftp = FTPHelper(ip=ip, password=pwd, port=port, username=user)

                        remote_path = ftp.create_dir(_date, remote_path="/data/report")
                        remote_path = ftp.create_dir(_time, remote_path)

                        ftp.upload_folder(root, remote_path)
                        ftp.close()

                        if Settings.ReportRemove:
                            for file in files:
                                os.remove(os.path.join(root, file))
                            os.removedirs(root)

                        dirs = os.path.join(remote_path, "ant")
                        dirs = dirs.replace("\\", "/")

                    client.send(("SUCCESS|%s|%s" % (dirs,json.dumps(summary))).encode(encoding='utf-8'))
                else:
                    client.send("FAILED".encode(encoding='utf-8'))
                logger.info(
                    f"********************************************Procedure is over,containing execution and uploading********************************************")
                client.close()
            self.client_pools.remove(client)
            break



#     # 主线程逻辑
#     while True:
#         cmd = input("""--------------------------
# 输入1:查看当前在线人数
# 输入2:给指定客户端发送消息
# 输入3:关闭服务端
# """)
#         if cmd == '1':
#             print("--------------------------")
#             print("当前在线人数：", len(g_conn_pool))
#         elif cmd == '2':
#             print("--------------------------")
#             index, msg = input("请输入“索引,消息”的形式：").split(",")
#             g_conn_pool[int(index)].sendall(msg.encode(encoding='utf8'))
#         elif cmd == '3':
#             exit()
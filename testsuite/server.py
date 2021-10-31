import json
import os
import socket
import datetime
from testsuite.runner import execute
from tools.FtpUtils import FTPHelper
from tools.logger import Logger
from tools.ReadConfig import ReadConfig
from config.settings import Settings

logger = Logger("Websocket server")


def server():
    """
    程序启动的主入口，只要启动websocket的监听服务后，客户端向服务端发送大执行的数据，则server端开始执行用例，并将生成的测试报告
    report/ant目录下的测试文件传输到对应的FTP服务器，之后将FTP服务器上的存储路径发送给客户端，客户端并从存储FTP上下载对应的报告，
    并在一个缓存路径下，之后再HTML中展示测试报告  #todo:需支持多线程处理多个客户端的数据
    """
    ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        ser.bind(ReadConfig.getWebsocket())
        ser.listen(5)
    except Exception as e:
        logger.error(f"Fail to start socket server with info [{ReadConfig.getWebsocket()}],error as follows:{str(e)}")
    else:
        logger.info(f"Websocket server [{ReadConfig.getWebsocket()}] is running.....")

        while True:
            client, addr = ser.accept()
            logger.debug(
                'Client: %s has connected at %s' % ((addr,), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            data = client.recv(Settings.websocket_server_allowed_size)

            data = data.decode(encoding="utf-8")
            logger.debug(f"""Server received data is:
    {data}
    """)
            data = json.loads(data)

            start = datetime.datetime.now()
            logger.info(f"Start to execute work at {start.strftime('%Y-%m-%d %H:%M:%S')}")

            flag = execute(data)

            end = datetime.datetime.now()
            logger.info(f"The execution ends at {start.strftime('%Y-%m-%d %H:%M:%S')},and duration is {end - start}")

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

                    for file in files:
                        os.remove(os.path.join(root, file))
                    os.removedirs(root)

                    dirs = os.path.join(remote_path, "ant")
                    dirs = dirs.replace("\\", "/")

                client.send(("SUCCESS|%s" % dirs).encode(encoding='utf-8'))

            else:
                client.send("FAILED".encode(encoding='utf-8'))
            client.close()


if __name__ == "__main__":
    server()

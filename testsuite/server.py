#coding=utf-8

import json
import os
import socket
import datetime
from tools.FtpUtils import FTPHelper
from tools.logger import Logger
from tools.ReadConfig import ReadConfig
from config.settings import Settings
from testsuite.runner import yield_pytest_exe

logger = Logger("Socket server")


def server():
    """
    start an socket server ,and will wait for a client to connect,the execute pytest main function,and will generate a
    report with a way of html file! The html file will be upload to Ftp server,and then return an ftp dirs path.The client
    will download the report according to the received dirs path to a temp report,and then with the method of loading frame,
    the content of html file will be displayed on web!
    """
    ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        ser.bind(ReadConfig.getWebsocket())
        ser.listen(5)
    except Exception as e:
        logger.error(f"Fail to start socket server with info [{ReadConfig.getWebsocket()}],error as follows:{str(e)}")
    else:
        logger.info(f"Socket server [{ReadConfig.getWebsocket()}] is running.....")

        while True:
            client, addr = ser.accept()
            logger.debug(
                'Client: %s has connected at %s' % ((addr,), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            data = client.recv(Settings.websocket_server_allowed_size)

            data = data.decode(encoding="utf-8")
            logger.debug(f"Server received data is:{data}")

            data = json.loads(data)

            start = datetime.datetime.now()
            logger.info(f"Start to execute work at {start.strftime('%Y-%m-%d %H:%M:%S')}")

            pytest_obj = yield_pytest_exe().__next__()
            flag = pytest_obj.execute(data)

            end = datetime.datetime.now()
            logger.info(f"The execution ends at {end.strftime('%Y-%m-%d %H:%M:%S')},and duration is {(end - start).seconds}")

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

                client.send(("SUCCESS|%s" % dirs).encode(encoding='utf-8'))

            else:
                client.send("FAILED".encode(encoding='utf-8'))
            logger.info(f"Procedure is over,containing execution and uploading!")
            client.close()


if __name__ == "__main__":
    server()

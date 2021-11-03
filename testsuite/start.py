
import json
import os
import socket
import socketserver
import datetime
from tools.FtpUtils import FTPHelper
from tools.logger import Logger
from tools.ReadConfig import ReadConfig
from config.settings import Settings
logger = Logger("Socket start server")


class SocketHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            self.data = self.request.recv(Settings.websocket_server_allowed_size)
            if not self.data : break

            data = self.data .decode(encoding="utf-8")
            logger.debug(f"Server received data is:{data}")

            data = json.loads(data)

            start = datetime.datetime.now()
            logger.info(f"Start to execute work at {start.strftime('%Y-%m-%d %H:%M:%S')}")

            try:
                from testsuite.runner import yield_pytest_exe

                pytest_obj = yield_pytest_exe().__next__()
                flag = pytest_obj.execute(data)

                end = datetime.datetime.now()
                logger.info(f"The execution ends at {end.strftime('%Y-%m-%d %H:%M:%S')},and duration is {end - start}")

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
            except Exception:
                self.feedback_data = ("FAILED".encode(encoding='utf-8'))
            else:
                self.feedback_data =("SUCCESS|%s" % dirs).encode(encoding='utf-8')
            finally:
                self.request.sendall(self.feedback_data)

def start():
    server = socketserver.ThreadingTCPServer(ReadConfig.getWebsocket(),SocketHandler)
    server.serve_forever()


if __name__ == "__main__":
    start()
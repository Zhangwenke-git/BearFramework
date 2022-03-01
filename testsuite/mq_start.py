import os
import json
import datetime
from tools.FtpUtils import FTPHelper
from tools.rabbitMQ import MQHandler
from config.settings import Settings
from tools.ReadConfig import ReadConfig
from testsuite.runner import yield_pytest_exe
mq = MQHandler()


def exec(channel, method, properties, body):
    pytest_obj = yield_pytest_exe().__next__()
    data = json.loads(body.decode())
    print(data)
    flag, summary = pytest_obj.execute(data)
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

            channel.basic_ack(delivery_tag=method.delivery_tag)



def main():
    mq.consume("report_processor_request", "report_build_request_routing_key", callback=exec)

if __name__ == "__main__":
    main()

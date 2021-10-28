import json
import os
import socket
import datetime
from shutil import copyfile

from testsuite.runner import run
from tools.logger import Logger
from tools.ReadConfig import ReadConfig
from config.settings import Settings


logger = Logger("Websocket server")

def server():
    ser=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ser.bind(ReadConfig.getWebsocket())
    ser.listen(50)

    logger.info(f"Start to run websocket server [{ReadConfig.getWebsocket()}]")

    while True:
        client,addr=ser.accept()
        logger.debug('Client: %s has connected at %s' % ((addr,),datetime.datetime.now().strftime("%Y-%m-%d HH:MM:SS")))
        data=client.recv(Settings.websocket_server_allowed_size)

        data = data.decode(encoding="utf-8")
        logger.debug(f"""Server received data is:
{data}
""")

        data = json.loads(data)
        flag = run(data)

        if flag:

            _date = datetime.datetime.now().strftime('%Y%m%d')
            _time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

            for root,dirs,files in os.walk(Settings.api_ant_report_path):

                for file in files:
                    report = os.path.join(Settings.FTP_DIR,_date,_time)
                    if os.path.exists(report):
                        pass
                    else:
                        os.makedirs(report)
                    copyfile(os.path.join(root,file),os.path.join(report,file))
                    os.remove(os.path.join(root,file))
            html = os.path.join(Settings.FTP_DIR, _date, _time)
            client.send(("SUCCESS|%s" % html).encode(encoding='utf-8'))

        else:
            client.send("FAILED".encode(encoding='utf-8'))
        client.close()

if __name__ == "__main__":
    server()
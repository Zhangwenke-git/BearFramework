import json
import socket
import datetime
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
            client.send("SUCCESS".encode(encoding='utf-8'))
        else:
            client.send("FAILED".encode(encoding='utf-8'))
        client.close()

if __name__ == "__main__":
    server()
import json

from tools.logger import Logger
import socket

logger = Logger("Websockets server")

def server():
    ser=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ser.bind(('127.0.0.1',5678))
    ser.listen(5)
    while True:
        client,addr=ser.accept()
        logger.debug('client: %s has connected!' % (addr,))
        data=client.recv(4096)

        data = data.decode(encoding="utf-8")
        logger.debug(f"Server received data is:{data}")

        from testsuite.runner import run

        data = json.loads(data)
        run(data)
        #
        # client.send("OK".encode(encoding='utf-8'))
        # client.close()

if __name__ == "__main__":
    server()
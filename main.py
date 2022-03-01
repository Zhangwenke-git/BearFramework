from testsuite.server import SocketServer
from threading import Thread


def main():
    server_ = SocketServer()
    server_.pre_process()
    server_.initializer()
    t = Thread(target=server_.accept_client())
    t.daemon=True
    t.start()


if __name__ == "__main__":
    main()
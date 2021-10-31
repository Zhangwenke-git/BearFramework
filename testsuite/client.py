import socket
import json
from tools.logger import Logger

logger = Logger("Websocket client")


def client(data):
    mysocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    mysocket.connect(('127.0.0.1',5678))

    data = json.dumps(data,indent=4,ensure_ascii=False)
    data = data.encode(encoding='utf-8')
    flag = False
    mysocket.send(data)
    while True:
        result=mysocket.recv(1024)
        if result:
            result = result.decode(encoding='utf-8')
            logger.info(f"The execution result is: [{result}]")
            if result == "SUCCESS":
                flag=True
        else:
            break
    mysocket.close()
    return flag


if __name__ == "__main__":
    from data.case import data_mapping_dict

    data = [
                    {
                        "module": "KMS",
                        "class_title": "秘钥管理系统",
                        "case": "kms_user_login",
                        "case_title": "KMS用户登录",
                        "case_description": "KMS用户登录接口，涵盖用户名和用户密码",
                        "templates_name": "kms_login_api",
                        "url": "http://127.0.1.1:8080/login",
                        "method": 1,
                        "header": {
                            "Content-Type": "application/json"
                        },
                        "data": {
                            "check": 1,
                            "password": "{{password}}",
                            "username": "{{username}}"
                        },
                        "scenarios": [
                            [
                                {
                                    "password": "dsaddddddddd",
                                    "username": "admin"
                                },
                                "用户名正确密码错误",
                                {
                                    "code": 200,
                                    "result": False,
                                    "message": " 密码错误"
                                }
                            ],
                            [
                                {
                                    "password": " sdad@1332",
                                    "username": "admin"
                                },
                                "用户名和密码均正确",
                                {
                                    "code": 200
                                }
                            ]
                        ]
                    }
                ]
    client(data)
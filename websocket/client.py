import socket
import json
#socket通信客户端
def client(data):
    mysocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    mysocket.connect(('127.0.0.1',5678))

    data = json.dumps(data,indent=4,ensure_ascii=False)
    data = data.encode(encoding='utf-8')

    mysocket.send(data)
    while True:
        data=mysocket.recv(1024)
        if data:
           print(data)
        else:
            break
    mysocket.close()

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
                            {
                                "parameter": {
                                    "password": "dsaddddddddd",
                                    "username": "admin"
                                },
                                "name": "用户名正确密码错误",
                                "validator": {
                                    "code": 200,
                                    "result": False,
                                    "message": " 密码错误"
                                }
                            },
                            {
                                "parameter": {
                                    "password": " sdad@1332",
                                    "username": "admin"
                                },
                                "name": "用户名和密码均正确",
                                "validator": {
                                    "code": 200
                                }
                            }
                        ]
                    }
                ]



    client(data_mapping_dict)
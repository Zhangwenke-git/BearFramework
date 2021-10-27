# -*-coding=utf-8-*-    
null = None
false = False
true = True

data_mapping_dict = [
    {
        "module": "UUMS",
        "class_title": "UUMS用户认证系统",
        "case": "uums_login",
        "case_title": "uums用户中心登录",
        "case_description": "uums用户中心登录",
        "templates_name": "uums用户中心登录模板",
        "url": "https://www.sojson.com/",
        "method": 1,
        "header": {
            "Content-Type": "application/json"
        },
        "data": {
            "username": "{{name}}",
            "passcode": "{{passcode}}"
        },
        "scenarios": [
            [
                {
                    "name": "ribn",
                    "passcode": "aaaa1111!"
                },
                "账号不存在密码正确",
                {
                    "code": 10032,
                    "result": " false",
                    "message": "用户不存在"
                }
            ],
            [
                {
                    "name": "猪宝宝",
                    "passcode": "aaaa1111!"
                },
                "登录账号和密码正确",
                {
                    "code": 200,
                    "result": "sussess"
                }
            ]
        ]
    },
    {
        "module": "KMS",
        "class_title": "KMS系统",
        "case": "login_kms",
        "case_title": "KMS用户登录接口",
        "case_description": "KMS用户登录接口",
        "templates_name": "kms登录模板",
        "url": "http://119.123.2.1:8980/login",
        "method": 1,
        "header": {
            "Content-Type": "application/json"
        },
        "data": {
            "id": "12324235545",
            "params": {
                "name": "{{username}}",
                "passcode": "{{password}}",
                "check": "${check}|<{{remember_flag}}>"
            }
        },
        "scenarios": [
            [
                {
                    "password": " sdad@1332",
                    "username": "zhangwenke",
                    "remember_flag": "true"
                },
                "用户正确密码错误",
                {
                    "code": 200
                }
            ],
            [
                {
                    "password": "aaaa1111!",
                    "username": "zhangwenke",
                    "remember_flag": "true"
                },
                "用户密码均正确",
                {
                    "code": 200
                }
            ]
        ]
    }
    # {
    #     "module": "ODM",
    #     "class_title": "ODM交易系统",
    #     "case": "order_submit",
    #     "case_title": "限价订单提交",
    #     "case_description": null,
    #     "templates_name": "现券XBOND订单提交",
    #     "url": "https://www.cnblogs.com/aaronthon/ajax/GetPostStat",
    #     "method": 1,
    #     "header": {
    #         "content-type": "application/json",
    #         "Authorization": "9480295ab2e2eddb8"
    #     },
    #     "data": {
    #         "ordrData": {
    #             "clntQtCd": "",
    #             "stlmntSpdNm": 2,
    #             "cntngncyIndctr": "",
    #             "flxblNetPrc": "",
    #             "qtTp": "${login}|<{{username}},{{password}}>",
    #             "netPrc": "{{netPrc}}",
    #             "instnCd": "{{instnCd}}",
    #             "nmnlVol": "{{volumn}}",
    #             "ordrTpIndctr": "1"
    #         }
    #     },
    #     "scenarios": [
    #         [
    #             {
    #                 "netPrc": "100.2344",
    #                 "password": "aaaa1111!",
    #                 "instnCd": "100035",
    #                 "volumn": "1000,000",
    #                 "username": "zhangwneke"
    #             },
    #             "限价订单提交-T+1",
    #             {
    #                 "code": 200,
    #                 "result": " sussess"
    #             }
    #         ]
    #     ]
    # }
]

import configparser
from config.settings import Settings

web_config = configparser.ConfigParser()
web_config.read(Settings.conf_path)


class ReadConfig:

    @staticmethod
    def getTimer():
        return web_config.get("timePoint", "point")

    @staticmethod
    def getReportStyle():
        return web_config.get("reportStyle", "reportFlag")

    @staticmethod
    def getCaseStyle():
        return web_config.get("apiCaseStyle", "caseStyle")

    @staticmethod
    def getWebsocket():
        ip = web_config.get("websocket", "ip")
        port = web_config.get("websocket", "port")
        return ip,int(port)

    @staticmethod
    def getFtp():
        ip=web_config.get("ftp","ip")
        port=web_config.get("ftp","port")
        username=web_config.get("ftp","username")
        password=web_config.get("ftp","password")
        return (ip,int(port),username,password)


    @staticmethod
    def read_db_info():
        host = web_config.get("DATABASE","host")
        username = web_config.get("DATABASE","username")
        password = web_config.get("DATABASE","password")
        database = web_config.get("DATABASE","database")
        port = web_config.getint("DATABASE","port")
        return host,username,password,database,port

    @staticmethod
    def read_mq_info():
        host = web_config.get("MQ","host")
        user = web_config.get("MQ","user")
        password = web_config.get("MQ","password")
        virtual_host = web_config.get("MQ","virtual_host")
        exchange = web_config.get("MQ","exchange")
        port = web_config.getint("MQ","port")
        return host,user,password,virtual_host,exchange,port
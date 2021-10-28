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
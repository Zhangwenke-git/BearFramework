from tools import logger
import configparser
logger= logger.Logger("Init_Env")
from config.settings import Settings
from tools.FileUtils import FileUtils
from tools.ReadConfig import ReadConfig
from tools.DictUtil import DictUtils


baseinfo = {
    'environment':"UAT4",
    'server_ip':"127.0.0.1",
    'timed_point':ReadConfig.getTimer(),
}



class Init_Env:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(Settings.conf_path,encoding="utf-8")
        self.data = dict(dict(config._sections)["environmentID"])
        self.data=DictUtils()._multiDictMerge([self.data,baseinfo])

    def dict_to_xml(self):
        parameter = []
        for k in sorted(self.data.keys()):
            xml = []
            v = self.data.get(k)
            if k == 'detail' and not v.startswith('<![CDATA['):
                v = '<![CDATA[{}]]>'.format(v)
            xml.append('<key>{value}</key>'.format(value=k))
            xml.append('<value>{value}</value>'.format(value=v))
            parameter.append('<parameter>{}</parameter>'.format(''.join(xml)))
        return '<environment>{}</environment>'.format(''.join(parameter))

    def init(self,xmlpath):
        data = self.dict_to_xml()
        folder_path = xmlpath[:-15]
        FileUtils().createFolder(folder_path)
        FileUtils().createFile(xmlpath)

        with open(xmlpath, 'w') as f:
            f.write(data)
            f.close()
        #logger.info("Initiate environment config file successfully!")



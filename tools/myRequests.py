import requests
from requests.adapters import HTTPAdapter
from tools import logger
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

logger = logger.Logger("API_request")
globals = {
    "true": True,
    "null": None,
    "false": False
}


class MyRequests(object):

    def __init__(self, timeout=5):
        reqObj = requests.Session()
        reqObj.mount('http://', HTTPAdapter(max_retries=3))
        reqObj.mount('https://', HTTPAdapter(max_retries=3))

        reqObj.verify = False
        self.reqObj = reqObj
        self.timeout = timeout



    def get(self, url, query_dict, headers, flag=False):
        result = self.reqObj.get(url, headers=headers, params=query_dict)
        if result.status_code == 200:
            logger.debug(f"Request successfully!")
            if flag:
                return eval(result.text, globals)
            else:
                return result
        else:
            logger.error(f"Fail to get request,response code is: {result.status_code}")

    def post(self, url, headers, form_data=None, body_dict=None, flag=False):
        """
        :function: post请求
        :param url:
        :param headers:
        :param form_data:
        :param body_dict:
        :param flag: 是否显示返回的response文本
        :return:
        """
        if form_data:
            result = self.reqObj.post(url, headers=headers, data=form_data)
            if result.status_code == 200:
                if flag:
                    logger.debug(f"Request successfully!")
                    return eval(result.text, globals)
                else:
                    return result
            else:
                logger.error(f"Fail to request,response code is: {result.status_code}")

        if body_dict:
            result = self.reqObj.post(url, headers=headers, json=body_dict)
            if result.status_code == 200:
                if flag:
                    logger.debug(f"Request successfully!")
                    return eval(result.text, globals)
                else:
                    return result
            else:
                logger.error(f"Fail to request,response code is: {result.status_code}")

    def __del__(self):
        if self.reqObj:
            self.reqObj.close()


if __name__ == "__main__":
    data = {'header': {'dplcF': 12, 'erCd': '55', 'erMsg': 'rg', 'lang': 'yy', 'msgSndngTm': 'ss', 'msgSrcEnd': 0, 'msgUuid': 'd3581dce-feb2-11df-dadf-8c35f29cfc6e', 'sesnId': '84efc9487ee17507e4bffc416d338400f2f36a55acb76298d4e876af90b106fb', 'sndrCmpntId': '100035', 'sndrSubId': '6270', 'tgtCmpntId': '111', 'tgtSubId': '11', 'tpcNm': 'ee', 'tstMdF': 22, 'srvcId': 4091001}, 'ordrData': {'clntQtCd': '', 'stlmntSpdNm': '1', 'cntngncyIndctr': None, 'flxblNetPrc': None, 'trdAcntCnShrtNm': '中信证券', 'qtTp': '5', 'netPrc': 1002222, 'instnCd': '100035', 'nmnlVol': 2000000, 'ordrTpIndctr': '1', 'trdrCd': '6270', 'dir': 'S', 'traTlCd': '140210', 'bndsNm': '14国开10', 'userRefInfo': {'key': '1', 'vl': '2'}, 'prdctCd': 'CBT', 'stlmntDt': '2020/07/07', 'clrngMthd': '2', 'isrCd': '100034', 'qtSrc': '0', 'trdngAcntCd': '100035', 'srNoId': '138', 'trdAcntSrNo': '2839', 'dlrSqncNoId': '2973', 'instnSrno': '576', 'ordrCd': '', 'flxblSpd': '', 'dtCnfrm': '20200707', 'alctnIndctr': '0'}, 'cbtOrdrData': {'yldToMrty': '5.2312', 'exrcsYld': '', 'bondTpNm': '政策性金融债', 'ttm': '275D', 'flxblExrcsYld': '', 'flxblYldToMrty': '', 'acrdIntrst': '1.38331', 'prmrktBondF': '0'}}

    header = {'accept-language': 'zh-CN', 'content-type': 'application/json; charset=UTF-8', 'authorization': '84efc9487ee17507e4bffc416d338400f2f36a55acb76298d4e876af90b106fb', 'cfetszoom': '6FA9ADE70802781C7E995A064E714C8F0C6002EF', 'Origin': 'https://199.31.191.38', 'Referer': 'https://199.31.191.38/node_modules/@ctaf/rmb-page/index.html', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}

    url = 'https://199.31.191.38/odm/orderEntry/cbt'

    obj = MyRequests()
    d = obj.post(url, headers=header,body_dict=data)
    print(d.cookies)
    print(d.status_code)
    print(dir(d))
    print(d.json())

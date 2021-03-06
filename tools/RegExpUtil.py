import re
from tools.logger import Logger

logger = Logger("RegExpUtil")


class RegExpUtil(object):

    @staticmethod
    def parse_result(result):
        if result:
            result = True
        else:
            result = False
        return result

    @staticmethod
    def match(pattern, string):
        """
        :function: 从字符串的开头曲匹配，主要是判断字符串是否以一个要求进行匹配的
        :param pattern:
        :param string:
        :return: True or False
        """
        result = re.match(pattern, string)
        return RegExpUtil.parse_result(result)

    @staticmethod
    def search(pattern, string, ignore_case=False):
        """
        :function:全文匹配，若有多个，只匹配第一个
        :param pattern:
        :param string:
        :param ignore_case: 是否忽略大小写
        :return:
        """
        flags = 0
        if ignore_case:
            flags = re.I
        return re.search(pattern, string, flags)

    @staticmethod
    def findAll(string, pattern, mult_flag=False):  # r'\{.*\S\}'    #  r'\{(?:.|\n)*\S\}'
        """
        :function: 查找所有满足要求的字符串，以一个list返回
        :param pattern:
        :param string:
        :return:
        """
        if len(string) == 0:
            logger.debug('The string is blank and fail to regex match!')
            re_list = []
        else:
            if mult_flag:
                comment = re.compile(pattern, re.DOTALL)
                re_list = comment.findall(string)
            else:
                re_list = re.findall(pattern=pattern, string=string)
            logger.debug(f"Success to regular match {len(re_list)} in total!")
        return re_list

    @staticmethod
    def replace_all(pattern, repl, string):
        """
        :function: 替换特殊字符
        :param pattern:
        :param repl:
        :param string:
        :return:
        """
        return re.sub(pattern, repl, string)


def replaceCharEntity(htmlstr):
    CHAR_ENTITIES={'nbsp':'','160':'',
                    'lt':'<','60':'<',
                    'gt':'>','62':'>',
                    'amp':'&','38':'&',
                    'quot':'"''"','34':'"'}
    re_charEntity=re.compile(r'&#?(?P<name>\w+);') #命名组,把 匹配字段中\w+的部分命名为name,可以用group函数获取
    sz=re_charEntity.search(htmlstr)
    while sz:
        key=sz.group('name') #命名组的获取
        try:
            htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1) #1表示替换第一个匹配
            sz=re_charEntity.search(htmlstr)
        except KeyError:
            htmlstr=re_charEntity.sub('',htmlstr,1)
            sz=re_charEntity.search(htmlstr)
    return htmlstr

def filter_tag(htmlstr):
    re_cdata = re.compile('<!DOCTYPE HTML PUBLIC[^>]*>', re.I)
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I) #过滤脚本
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I) #过滤style
    re_br = re.compile('<br\s*?/?>')
    re_h = re.compile('</?\w+[^>]*>')
    re_comment = re.compile('<!--[\s\S]*-->')
    s = re_cdata.sub('', htmlstr)
    s = re_script.sub('', s)
    s=re_style.sub('',s)
    s=re_br.sub('\n',s)
    s=re_h.sub(' ',s)
    s=re_comment.sub('',s)
    blank_line=re.compile('\n+')
    s=blank_line.sub('\n',s)
    s=re.sub('\s+',' ',s)
    s=replaceCharEntity(s)
    return s






# 匹配特定的字符串 "abc"

# re_pattern=r'abc'

# 从'qwvugiguuihabchuwiiih'这个字符串当中匹配是否有 re_pattern
# match表示：从开始的位置进行匹配
# res=re.match(re_pattern,'abcqwvugiguuihabchuwiiih')
# print(res)

# search  全文匹配  若有多个匹配第一个
# res=re.search(re_pattern,'qwvugiguuihabchuwiiih')
# print(res)

# findall  全部匹配  常用场景：爬虫
# res=re.findall(re_pattern,'abcqwvugiguuihabchuwiiih')
# print(res)

# [abc]  匹配中括号中的任意一个字符
# re_pattern=r'[abc]'
# res=re.findall(re_pattern,'abcqwvugiguuihabchuwiiih')
# print(res)

# [a-z], 匹配中括号中的而任意一个字符
# re_pattern = '{m, n}'
# res = re.findall(re_pattern, "abcwofowpqfowfjowefjiwoefabcowof")
# print(res)

# . 匹配任意的一个字符串， 除了 \n换行符
# re_pattern = r'.'
# res = re.findall(re_pattern, "a\nbcwofowpqfowfjowefjiwoefabcowof")
# print(res)

# \d  匹配数字 data
# re_pattern = r'\d'
# res = re.findall(re_pattern, "a123bcwofowpqfowfjowefjiwoefabcowof")
# print(res)

# \D  匹配非数字 data
# re_pattern = r'\D'
# res = re.findall(re_pattern, "a@123bcwofowpqfowfjowefjiwoefabcowof")
# print(res)

# \w  匹配字母，数字，下划线
# re_pattern = r'\w'
# res = re.findall(re_pattern, "a@_123bcwofowpqfowfjowefjiwoefabcowof")
# print(res)

# \W 反向的， 非

#  匹配花括号当中的数字次，  匹配几次，
# re_pattern = r'\d{2}'
# res = re.findall(re_pattern, "aa@_123b&cwofowpqfowfjowefjiwoefabcowof")
# print(res)

#  {2, } 匹配至少 2 次
# TODO: 正则表达式当中，千万不要手残，空格不能随便打
# 贪婪模式， python 当中
# re_pattern = r'\w{2,}'
# res = re.findall(re_pattern, "aa@_123b&cwofowpqfowfjowefjiwoefabcowof")
# print(res)

# {,2} 匹配最多 2 次
# re_pattern = r'\w{,2}'
# res = re.findall(re_pattern, "aa@_123b&cwofowpqfowfjowefjiwoefabcowof")
# print(res)

# {2,4} 匹配 2 -4 次
# re_pattern = r'\w{2,4}'
# res = re.findall(re_pattern, "aa@_123b&cwofowpqfowfjowefjiwoefabcowof")
# print(res)

# 如果去匹配一个手机号码
# re_pattern = r'1[35789]\d{9}'
# res = re.findall(re_pattern, "aa@_123b&cw18711111111ofjoabcowof")
# print(res)
# 邮箱号码

#  *  匹配0次或者任意次，表示通配符
# re_pattern = r'\d*'
# res = re.findall(re_pattern, "aa@_123b&cw18711111111ofjoabcowof")
# print(res)

#  +  匹配一次或者任意次
# re_pattern = r'\d+'
# res = re.findall(re_pattern, "aa@_123b&cw18711111111ofjoabcowof")
# print(res)

#  . 组合
# re_pattern = r'\d.'
# res = re.findall(re_pattern, "aa@_123b&cwo17520208510fowpqfowfjowefjiwoefabcowof")
# print(res)

#  ? 匹配0次或者1次
# re_pattern = r'\d?'
# res = re.findall(re_pattern, "aa@_123b&cwo17520208510fowpqfowfjowefjiwoefabcowof")
# print(res)

#  ? 非贪婪模式，尽量少的匹配
# re_pattern = r'\d*?'
# res = re.findall(re_pattern, "aa@_123b&cwo17520208510fowpqfowfjowefjiwoefabcowof")
# print(res)

#  ^ 开头  匹配开头的数字
# re_pattern = r'^\d'
# res = re.findall(re_pattern, "1aa@_123b&cwo17520208510fowpqfowfjowefjiwoefabcowof")
# print(res)

# 结尾  匹配结尾数字
# re_pattern = r'\d$'
# res = re.findall(re_pattern, "iwoefabcowof243")
# print(res)

# 结尾  匹配结尾所有数字
# re_pattern = r'\d*$'
# res = re.findall(re_pattern, "iwoefabcowof243")
# print(res)

# mystr = '{"member_id": "#member_id#", "loan_id": "#loan_id#", "token": "#token#", "username": "#username#"}'
# # 匹配规则
# re_pattern = r'#(.*?)#'
# res = re.findall(re_pattern, mystr)
# print(res)
# 组
# 替换 re.sub() 替换操作
# mystr = re.sub(re_pattern, 'me123', mystr, 1)
# mystr = re.sub(re_pattern, 'loan123', mystr, 1)
# mystr = re.sub(re_pattern, 'tokenloan123', mystr, 1)
# print(mystr)

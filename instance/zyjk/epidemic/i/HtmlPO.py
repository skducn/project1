# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author     : John
# Date       : 2021-7-1
# Description: Html 对象层
# *******************************************************************************************************************************

'''
1，获取网站状态码
2，获取网站的headers
3，获取网页内容
4，生成headers和proxies代理
5，获取json网页内容
'''


from PO.DataPO import *
Data_PO = DataPO()

class HtmlPO:

    # 1，获取网站状态码
    def getCode(self, varUrl):
        try:
            response = requests.get(varUrl)
            return response.status_code
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 2，获取网站的header
    def getHeaders(self, varUrl):
        # {'Cache-Control': 'private, no-cache, no-store, proxy-revalidate, no-transform', 'Connection': 'Keep-Alive',
        #  'Content-Encoding': 'gzip', 'Content-Type': 'text/html', 'Date': 'Fri, 20 Sep 2019 07:12:16 GMT',
        #  'Last-Modified': 'Mon, 23 Jan 2017 13:23:55 GMT', 'Pragma': 'no-cache', 'Server': 'bfe/1.0.8.18',
        #  'Set-Cookie': 'BDORZ=27315; max-age=86400; domain=.baidu.com; path=/', 'Transfer-Encoding': 'chunked'}'''
        try:
            response = requests.get(varUrl)
            return response.headers
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")


    # 3，获取网页内容
    def getText(self, varUrl):
        try:
            res = requests.get(url=varUrl)
            # get请求时，response默认使用iso - 8859 - 1编码对消息体进行编码，如果返回内容出现乱码，可以使用 utf-8 , gb2312
            # 解决方法：查看网页源码找到charset关键字，如 charset=utf-8
            res.encoding = "utf-8"
            return res.text
        except:
            print("[ERROR], " + sys._getframe(1).f_code.co_name + ", line " + str(
                sys._getframe(1).f_lineno) + ", in " + sys._getframe(
                0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")


    # 4，生成headers和proxies代理
    def getHeadersProxies(self):
        try:
            # self.headers = {'User-Agent': Data_PO.getUserAgent()}
            self.headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}

            varIp = Data_PO.getIpAgent()
            self.proxies = {str(varIp).split("://")[0]: str(varIp).split("://")[1]}
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")


    # 5，获取json网页内容
    def getJson(self, varUrl):
        try:
            self.session = requests.session()
            response = requests.get(url=varUrl, headers=self.headers, proxies=self.proxies)
            return response.json()
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")


    # 6，解析session.get
    def sessionGet(self, varUrl):
        try:
            self.session = requests.session()
            ir = self.session.get(varUrl, headers=self.headers)
            return ir
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")





if __name__ == '__main__':

    Html_PO = HtmlPO()


    print("1，获取网站状态码".center(100, "-"))
    print(Html_PO.getCode("http://www.baidu.com"))


    print("2，获取网站的headers".center(100, "-"))
    print(Html_PO.getHeaders("http://www.baidu.com"))


    print("3，获取网页内容".center(100, "-"))
    print(Html_PO.getText("http://www.baidu.com"))


    # print("4，生成headers和proxies代理".center(100, "-"))

    print("5，获取json网页内容".center(100, "-"))
    Html_PO.getHeadersProxies()
    print(Html_PO.getJson("https://www.ximalaya.com/revision/album/getTracksList?albumId=13738175&pageNum=1"))

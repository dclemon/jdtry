# -*- coding: utf-8 -*-
import requests
import time
import random
import json
import re
from bs4 import BeautifulSoup
import configparser
import os
import datetime

ftkey = ''
class jdobj:
    def __init__(self):
        self.name = ""
        self.time = 0
        self.amount = ""
        self.activeid = ""
        self.price = ""
def getmidstring(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()
def write_ini(inikey, inivaluse, str):
    config = configparser.ConfigParser()
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    config.read(parent_dir  + "/info_date.ini", encoding = 'utf-8')
    convaluse = config.set(inikey, inivaluse, str)
    config.write(open(parent_dir + "/info_date.ini", "w"))
    return convaluse
def read_ini(inikey, inivaluse, filepath):
    config = configparser.ConfigParser()
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    config.read(parent_dir  + "/" + filepath,encoding = 'utf-8')
    convaluse = config.get(inikey, inivaluse)
    return convaluse
class jdtry:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'ContentType': 'text/html; charset=utf-8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'script',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-site',
            'Accept': '*/*',
        }
        self.sess = requests.Session()
        self.cookies = {

        }
    def check_login(self):
        now_time = datetime.datetime.now()
        print ('当前时间' + str(now_time) + "正在检测登录状态！")
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        with open(parent_dir + '/cookie.txt', 'r') as f:
            cokstr = f.read()
            print(cokstr)
            cookie = eval(cokstr)

            # 测试新cookie
        # 格式有效
        # 注意点1.分号改逗号2.等号改冒号3.加双引号
        url = 'https://try.m.jd.com/isLogin'
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'ContentType': 'text/html; charset=utf-8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'authority': 'try.m.jd.com',
            'method': 'GET',
            'path': '/isLogin',
            'scheme': 'https',
            'x-requested-with': 'XMLHttpRequest',
            'Referer': 'https://try.m.jd.com/user?jdreactkey=JDReactOnTrialChannel&jdreactapp=JDReactOnTrialChannel&transparentenable=true&page=myTrial&ptag=138725.8.1&jdreactAppendPath=user'
        }
        res = requests.get(url, headers=head, cookies=cookie)
        c = json.loads(res.text)
        print(c)
        d = c['isLogin']
        return d
  
    def get_price(self, product_list):
        now_time = datetime.datetime.now()
        print ('当前时间' + str(now_time) + '正在查询价格')
        for i in range(len(product_list)):
            sku_id = product_list[i].skuid
            url = "https://p.3.cn/prices/mgets?skuIds=" + sku_id + "&origin=2"
            head = {
                'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
                'Connection': 'keep-alive',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, sdch',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Host': 'p.3.cn',
                'Referer': 'https://book.jd.com/booktop/0-0-0.html?category=1713-0-0-0-10001-1'
            }
            self.headers = head
            for n in range(5):
                try:
                    res = requests.get(url, headers=head)
                    break
                except requests.exceptions.RequestException as e:
                    print(e)
            jsStr = res.content
            jsonArr = json.loads(jsStr)
            try:
                product_list[i].price = getmidstring(str(jsonArr[0]), "'p': '", "'")
            except:
                print('該商品沒有給出價格，刪去商品！')
                product_list[i].price = '0'
                break
        return product_list
    def try_post(self, plan):
        # 申请试用
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        with open(parent_dir + '/cookie.txt', 'r') as f:
            cokstr = f.read()
            cookie = eval(cokstr)
        head = self.headers
        head['Host'] = 'try.jd.com'
        head['Referer'] = 'https://try.m.jd.com/'
        # head['Host'] = 'try.jd.com'
        # head['Referer'] = 'https://try.m.jd.com/'
        head['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        #先看看有没有申请过
        #https://try.m.jd.com/activity?jdreactkey=JDReactOnTrialChannel&jdreactapp=JDReactOnTrialChannel&jdreactAppendPath=activity&transparentenable=true&page=detail&from=m_page&ptag=138725.10.1&id=1324068
        url = "https://try.m.jd.com/activity?jdreactkey=JDReactOnTrialChannel&jdreactapp=JDReactOnTrialChannel&jdreactAppendPath=activity&transparentenable=true&page=detail&from=m_page&ptag=138725.10.1&id=" + plan.activeid
        for n in range(5):
            try:
                res = requests.get(url, cookies=cookie)
                break
            except requests.exceptions.RequestException as e:
                print(e)

        a = getmidstring(str(res.content), "taskId", '}}')
        jsonArr = "{taskId"+a+"}}"
        temp = getmidstring(str(jsonArr), '"venderId":',',')
        # :{"venderId":770031,"title":"\xe7\xbd\x97\xe6\x8a\x80\xe7\x94\xb5\xe7\xab\x9e\xe6\x97\x97\xe8\x88\xb0\xe5\xba\x97","appName":"http://mall.jd.com/index-765880.html","fullLogo":"http://img30.360buyimg.com/popshop/jfs/t1/15498/36/5701/33064/5c414beeE26990c65/02e005151af36260.jpg","shopId":765880
        temp2 = getmidstring(str(jsonArr), '"data"','{')
        temp3 = getmidstring(str(jsonArr), '"submit":',',')
        temp4 = getmidstring(str(jsonArr), '"shopId":', '}')

        if temp == None:
            plan.isposted = True
        elif temp2 == None:
            plan.isposted = True
        elif temp3 == None:
            plan.isposted = True
        elif temp3 == "true":
            plan.isposted = True
        elif temp3 == "false":
            plan.isposted = False
        elif temp4 == None:
            plan.isposted = True
        if plan.isposted == True:
            return
        else:
            plan.shopid = temp4
            plan.venderId=temp
            head = self.headers
            head['Host'] = 'try.jd.com'
            head['Referer'] = 'https://try.m.jd.com/'
            for n in range(5):
                try:
                    url = 'https://try.m.jd.com/followShop?id=' + str(plan.shopid)
                    print(plan.shopid)
                    # 关注https://try.m.jd.com/followShop?id=10139217
                    res = requests.get(url, cookies=cookie)
                    jsonArr = json.loads(res.content)
                    print(jsonArr)
                    break
                except requests.exceptions.RequestException as e:
                    print(e)
            for n in range(5):
                try:
                    millis = int(round(time.time() * 1000))
                    url = 'https://try.jd.com/migrate/apply?activityId=' + plan.activeid + '&source=1&_s=m&_='+ str(millis) +'&callback=jsonp5'
                    # 申请
                    res = requests.get(url, headers=head, cookies=cookie)
                    s = res.text
                    time.sleep(5)
                    print(s)
                    break
                except requests.exceptions.RequestException as e:
                    print(e)
            if s.find("您的申请次数已超过上限") != -1:#不等于-1，即寻找到此文本,向微信报错
                for n in range(5):
                    try:
                        requests.get('https://sc.ftqq.com/' + ftkey + '.send?text=京东今日申请达到上限')
                        break
                    except requests.exceptions.RequestException as e:
                        print(e)
                return "申请次数已满"
            for n in range(5):
                try:
                    millis = int(round(time.time() * 1000))
                    # https://try.jd.com/migrate/unfollow?_s=pc&venderId=770171
                    # https://wq.jd.com/fav/shop/DelShopFav?shopId=774279&venderId=778235&_=1610947683210&sceneval=2&g_login_type=1&callback=jsonpCBKL&g_ty=ls
                    url = 'https://wq.jd.com/fav/shop/DelShopFav?shopId='+str(plan.shopid)+'&_='+str(millis)+'&sceneval=2&g_login_type=1&callback=jsonpCBKG&g_ty=ls'
                    # 取关
                    print(url)
                    head = {
                        "Host": "wq.jd.com",
                        "Accept": "*/*",
                        "Connection": "keep-alive",
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
                    'Referer': 'https://wqs.jd.com/my/fav/shop_fav.shtml?sceneval=2&jxsid=15960121319555534107&ptag=7155.1.9',
                    "Accept-Language": "zh-cn",
                    "Accept-Encoding": "gzip, deflate, br"
                    }
                    res = requests.get(url, headers=head, cookies=cookie)
                    print(res.text)
                    break
                except requests.exceptions.RequestException as e:
                    print(e)
        return
    def get_product_list(self):#获取试用商品列表,返回的uls是一个数组，每个成员内包含商品名称和编号skd_id
        cids_list = read_ini('appbase','cids_list','info.ini')
        cids_list = cids_list.split(',')
        uls = []
        for cids in cids_list:
            for page in range(15):
                url = "https://try.jd.com/activity/getActivityList?page=" + str(
                    page + 1) + '&cids=' + str(cids)  # &cids=1320通过cdds来确定分区
                time.sleep(0.2)
                for n in range(5):
                    try:
                        res = requests.get(url)
                        break
                    except requests.exceptions.RequestException as e:
                        print(e)
                html_str = res.text
                besoup = BeautifulSoup(html_str, features='lxml')
                div_str = str(besoup.find_all('div', attrs={'class': "con"}))
                items = BeautifulSoup(div_str, "html.parser")
                a = items.find_all('li')  # 类型：resultset
                uls.append(a)
        product = []
        p = len(uls)
        print('当前时间'+str(datetime.datetime.now())+'正在查询商品')
        for o in range(p):
            for n in uls[o]:
                temp = jdobj()
                t1 = getmidstring(str(n), 'sys_time="', '"')  # 目前时间
                t2 = getmidstring(str(n), 'end_time="', '"')
                t3 = (int(t2) - int(t1)) / 3600000  # 剩余时间
                temp.name = getmidstring(str(n), '<div class="p-name">', '</div>')
                temp.time = t3
                temp.skuid = getmidstring(str(n), 'sku_id="', '"')
                temp.activeid = getmidstring(str(n), 'activity_id="', '"')
                temp.amount = getmidstring(str(n), '>提供<b>', '</b>份')
                product.append(temp)
        return product
    def rank(self, product_list):
        #第一步筛选价格
        #第二部筛选关键词
        #时间就不过滤了
        key_word_list = read_ini('appbase', 'key_word_list', 'info.ini')
        key_word_list = key_word_list.split(',')
        print (key_word_list)
        ex_price = read_ini('appbase', 'ex_price','info.ini')
        plan = []
        for temp in product_list:
            if float(temp.price) > float(ex_price):
                plan.append(temp)
        for temp in plan:
            for key_word in key_word_list:
                if temp.name.find(key_word) != -1:  # 有过滤词
                    plan.remove(temp)
                    break
        return plan




def get_try():
    now_time = datetime.datetime.now()
    print ('当前时间' + str(now_time) + "开始执行京东试用脚本！")
    jd = jdtry()

    while jd.check_login() == False:
        requests.get('https://sc.ftqq.com/' + ftkey + '.send?text=京东cookie已失效')
        print ('cookie失效，请更新')
        time.sleep(3600)
    else:
        print ('登录有效')
        product = jd.get_product_list()
        product = jd.get_price(product)
        product = jd.rank(product)
        for n in range(5):
            try:
                requests.get('https://sc.ftqq.com/' + ftkey + '.send?text=预计最大申请数量：'+str(len(product)))
                break
            except requests.exceptions.RequestException as e:
                print(e)
        for plan in product:
            res = jd.try_post(plan)#一条一条申请
            if res == "申请次数已满":
                return
        #跑完全部任务都没跑满
        requests.get('https://sc.ftqq.com/' + ftkey + '.send?text=今日京东未跑满')
        return
# 737,9987,670,1620,1316,1325,12218,5025,12259
def run ():
    last_date = read_ini("appbase", "last_date", 'info_date.ini')
    now_time = datetime.datetime.now()
    now_date = now_time.strftime('%x')
    print (last_date,now_date)
    if now_date != last_date:

        get_try()
        write_ini("appbase", "last_date", str(now_date))
        print (str(now_time) + "今日申请完毕，待机1小时。")
        time.sleep(3600)
    else:
        print (str(now_time) + "今日已经申请过，待机中。")
        jd = jdtry()
        jd.check_login()
        time.sleep(3600)
        return
    return
def main():
    while True:
        run()
    return
if __name__ == '__main__':
    main()

    

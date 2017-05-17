'''
Created on 2017年5月16日

@author: master-hadoop
'''
from multiprocessing import Pool
import os
import random
import time
from wsgiref import headers

from bs4 import BeautifulSoup
import requests



def IP_Test(IP, URL_test, set_timeout=1)  :# 测试IP地址是否可用,时间为3秒
    try:
        requests.get(URL_test, headers=headers, proxies={'http': IP}, timeout=set_timeout)
        return True
    except:
        return False


def get_IP_test(num_IP=10):
    IP_url = 'http://www.youdaili.net/Daili/http/19733.html' # 获取IP的网站
    test_url = 'http://33img.com/' # 测试IP是否可用的的网站
    wb_date = requests.get(IP_url, headers=headers)
    wb_date.encoding = 'utf-8'
    soup = BeautifulSoup(wb_date.text, 'lxml')
    IP = soup.select('div.arc > div.content > p > span')
    IP_list = []
    for i in IP:
        span_IP = i.get_text().encode('utf-8').split('@')[0]
        print (span_IP)
        if IP_Test(span_IP, test_url):  # 测试通过
            IP_list.append(span_IP)
            print ('测试通过，IP地址为 '+ str(span_IP))
        if len(IP_list) > num_IP - 1:  # 搜集够N个IP地址就行了
            print('搜集到' + str(len(IP_list)) + '个合格的IP地址')
            return IP_list
    return IP_list

# for i in get_IP_test():
#     print i

IP_list = [
    '58.221.75.7:8888',
    '222.35.74.60:80',
    '58.68.226.186:80',
    '175.6.10.12:8888',
    '58.221.75.145:8888',
    '210.72.95.134:80',
    '117.36.73.83:80',
    '117.34.47.7:8888',
    '123.234.8.210:8080'
    
]
#http://bbs.1024v3.pw/pw/thread.php?fid=22&page=1
def get_1024_links(page):
    url = 'http://bbs.1024v3.pw/pw/thread.php?fid=5&page={}'.format(page)
    url1 = 'http://bbs.1024v3.pw/pw/'   #'http://pics.dmm.co.jp/'#'http://bbs.1024v3.pw/pw/'
    wb_data = requests.get(url)
    wb_data.encoding = 'utf-8' # 不然会乱码，老司机探过这个雷
    # print wb_data.text
    soup = BeautifulSoup(wb_data.text, 'html.parser') # 我习惯用lxml
    links = soup.select('tr.tr3 > td > h3 > a')
    links_1024 = []
    for link in links:
        url = url1 + link.get('href') # 拼接成帖子的链接
        print(url)
        links_1024.append(url)
    return links_1024 # 返回这一页50个帖子的链接列表

def get_format_filename(input_filename): # 文件夹的名字不能含有的特殊符号，windows下的限定
    for s in ['?', '*', '<', '>', '\★', '！', ':', '/']:
        while s in input_filename:
            input_filename = input_filename.strip().replace(s, '')
    return input_filename


def get_1024_details(url): # 这里接收get_1024_links返回的link链接列表
    wb_date = requests.get(url)
    wb_date.encoding = 'utf-8'
    soup = BeautifulSoup(wb_date.text, 'html.parser')
    #print '子页面读取完毕，开始尝试处理图片'
    pic_link = soup.select('#read_tpc > img')[0].get('src')
    pic = download_single_image(pic_link) # 用的是戴司机的download_single_image函数
    print(pic_link)
    if pic != None:
        filename = soup.select('#subject_tpc')[0].get_text()#.encode('utf-8')
        filename = get_format_filename(filename)#.decode('utf-8')
        if not os.path.exists(filename):# windows保存文件的坑，不然乱码
            os.makedirs(filename)
        pic = pic.content
        # with open(os.getcwd() + '//'+filename+'//' +filename + '.jpg', 'wb') as f:
        # with open(os.getcwd() + '//' + filename + '.jpg', 'wb') as f:
        try:
            with open(os.getcwd() + "//" + filename + "//" + filename + '.jpg', 'ab') as f:
                print('下载得到图片！保存图片''大小为'+str(len(pic)))
                f.write(pic)
            torrent_link = soup.select('#read_tpc > a')[0].get('href')
            get_torrent(torrent_link, filename)
        except IOError:
            print (url, filename) # 出错，返回出错链接跟文件名 http://bbs.1024v3.pw/pw/htm_data/5/1705/640026.html



def download_single_image(image_url, proxy_flag=False, try_time=0): # 首先尝试直接下载，一次不成功则尝试使用代理
    if not proxy_flag:#不使用代理
        try:
            image_html = requests.get(image_url, headers=get_image_header(), timeout=20)
            print('图片直接下载成功')
            time.sleep(1)
            return image_html #一次就成功下载！
        except:
            return download_single_image(image_url, proxy_flag=True)#否则调用自己，使用3次IP代理
    else: # 使用代理时
        if try_time < count_time:
            try:
                print('尝试第'+str(try_time+1)+'次使用代理下载')
                # IP_address=get_random_IP()[0]
                image_html = requests.get(image_url, headers=get_image_header(), proxies={'http': get_random_IP()}, timeout=20)
                print ('状态码为'+str(image_html.status_code))
                if image_html.status_code==200:
                    print('图片通过IP代理处理成功！')
                    return image_html  # 代理成功下载！
                else:
                    a= download_single_image(image_url, proxy_flag=True, try_time=(try_time + 1))
                    return a
            except:
                print('IP代理下载失败')
                a = download_single_image(image_url, proxy_flag=True, try_time=(try_time+1))  # 否则调用自己，使用3次IP代理
                return a
        else:
            print ('图片未能下载' + image_url)
            return None
def get_torrent(torrent_link, filename):
    #http://www3.uptorrentfilespacedownhostabc.cloud/updowm/file.php/OPHF62s.html
    torrent_download_url = 'http://www3.uptorrentfilespacedownhostabc.rocks/updowm/down.php'#http://www3.uptorrentfilespacedownhostabc.pink/updowm/down.php
    s = requests.Session()
    wb_date = s.get(torrent_link, headers=get_request_headers())
    wb_date.encoding = 'utf-8'
    soup = BeautifulSoup(wb_date.text, 'html.parser')
    data = {}
    for i in soup.select('form input'):
        if i.get('name'):
            data[i.get('name')] = i.get('value')
            # print data
    torrent = s.post(torrent_download_url, headers=get_torrent_headers(), data=data)
    with open(os.getcwd() + '//'+ filename+'//' + filename + '.torrent', 'ab') as f:#open(a_path+'.txt', 'w')# r只读，w可写，a追加
        print('下载得到图片！保存图片'+str(filename)+'大小为'+str(len(torrent)))

        f.write(torrent.content)
if __name__ == '__main__':
    pool = Pool(processes=1)
    for i in range(2,3):
        print ('正在爬起第' + str(i) + '页')
        links = get_1024_links(i)
        try:
            pool.map(get_1024_details, links)
        except IndexError:
            pass
    pool.close()
    pool.join()   
    
UserAgent_List = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]


def get_request_headers():
    request_headers = {
        'User-Agent': random.choice(UserAgent_List),
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'Accept-Encoding': 'gzip',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        }
    return request_headers


def get_torrent_headers():
    torrent_headers = {
   
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Length':'36',
            'Content-Type':'application/x-www-form-urlencoded',
            'Cookie':'__cfduid=db364a512edc57151c9ba5af8a1bb1ced1494919719; a4184_pages=2; a4184_times=3',
            'Host':'http://www3.uptorrentfilespacedownhostabc.rocks/',
            'Origin':'http://www3.uptorrentfilespacedownhostabc.rocks/',
            'Referer':'http://www3.uptorrentfilespacedownhostabc.rocks/',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':random.choice(UserAgent_List),
    }
    return torrent_headers               
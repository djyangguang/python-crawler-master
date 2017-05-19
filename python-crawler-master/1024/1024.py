'''
批量下载1204图片

1024导航网站http://1024bug.me/
'''
import datetime
import random
import time
import urllib.request, socket, re, sys, os
from wsgiref import headers

from bs4 import BeautifulSoup
from pip._vendor.colorama.ansi import Style
import requests


num_IP=10
URL_IP='http://www.youdaili.net/Daili/http/19733.html'#获取IP的网站
IP_test_timeout=1#测试IP时超过多少秒不响应就舍弃了
#http://bbs.1024v3.pw/pw/
baseUrl='http://bbs.1024v3.pw/pw/'
#"F:\\xiezhen\\04" xiezhen
#"F:\\xiezhen\\zipai\\01" xiezhen
targetPath = "F:\\xiezhen\\zipai\\01" 
headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            'Accept-Encoding':'gzip',
           }#初始使用的header
def getContant(Weburl):
    Webheader= {'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36',}
    req = urllib.request.Request(url = Weburl,headers=Webheader)
    respose = urllib.request.urlopen(req)
    _contant = respose.read()
    respose.close()
    return str(_contant)
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
def getUrl(URL):
    #pageIndex = input("要下载多少页呢？\n")
    pageIndex = 1
    for i in range(1,int(pageIndex)+1):
#         Weburl = URL + str(i)#获取每大页的URL
        Weburl = URL
       # contant = getContant(Weburl)
       # comp = re.compile(r'<a href="htm_data.{0,30}html" ')#target="_blank" id=""><font color=g
      #  urlList1 = comp.findall(contant)
      #  comp = re.compile(r'a href="(.*?)"')
      #  urlList2 = comp.findall(str(urlList1))
        urlList = []
      #  for url1 in urlList2:# 地址拼接
      #      url2 = baseUrl+url1
       #     urlList.append(url2)
        start_html = requests.get(Weburl,  headers=headers)
        start_html.encoding='utf-8'
        bsObj = BeautifulSoup(start_html.text,'html.parser')
        for a in bsObj.find("tbody", {"style":"table-layout:fixed;"}).findAll("a"):
           if ('href' in a.attrs) and ('title' not in a.attrs ) :
               if re.match(r'^htm_data/.+.html', a.attrs['href']):
                   url2 = baseUrl+a.attrs['href']
                   urlList.append(url2)
        return urlList

def openUrl(url,x):
    headers = {
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '                            'Chrome/51.0.2704.63 Safari/537.36'
               }

    filePath=targetPath#+url[-12:-5]
    #检测当前路径的有效性
   # if not os.path.isdir(filePath):
       # os.mkdir(filePath)
#     req = urllib.request.Request(url=url, headers=headers)
#     res = urllib.request.urlopen(req)
#     data = res.read()
    start_html = requests.get(url, headers=headers)
    start_html.encoding='utf-8'
          
    data=BeautifulSoup(start_html.text,'html.parser')
    downImg(data,filePath,x)
#     image = download_single_image(data)
#     else:
#         print("已经下载过的地址跳过："+url)
#         print("filePath  "+filePath)

def downImg(data,filePath,x):
    img_ind = 1 
    for link,f in set(re.findall(r'([http|https]:[^\s]*?(jpg|png|gif))', str(data))):

#         if link.startswith('s'):
#             link='http'+link
#         else:
        link='htt'+link
       
        try:
            opener=urllib.request.build_opener()
#             opener.addheaders=[('User-Agent',random.choice(UserAgent_List))]
#             opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
#             urllib.request.install_opener(opener)
#             urllib.request.urlretrieve(link,saveFile(x,link,filePath))
#             now = datetime.datetime.now()
#             
#             print(now.strftime('%Y-%m-%d %H:%M:%S')+"=====>"+link)
            image = download_single_image(link,x,filePath)
            if image and len(image.content)>4000:  # 如果不是为空，则说明下载到了,另外图片如果太小，说明图片数据错误（全黑的），一般都是网站上这个图确实没数据
                os.chdir(filePath)
                now = datetime.datetime.now()
                now.strftime('%Y-%m-%d %H:%M:%S')  
                f = open(x+str(img_ind) + '.jpg', 'ab')
#                 print(now.strftime('%Y-%m-%d %H:%M:%S')+"========>" +link+"["+str(img_ind)+"]"+'大小为'+str(len(image.content)))         
                f.write(image.content)
                f.close()
            img_ind += 1 
        except:
            img_ind += 1 
            print('失败')
def IP_Test(IP,URL_test,set_timeout=IP_test_timeout):#测试IP地址是否可用,时间为3秒
    try:
        requests.get(URL_test, headers=headers, proxies={'http': IP[0] }, timeout=set_timeout)
        return True
    except:
        return False            
# def get_IPlist(URL,test_URl='http://www.33img.com/'):#获取可用的IP地址
#     IP_list=[]
#     start_html = requests.get(URL, headers=headers)
#     start_html.encoding = 'utf-8'
#     bsObj = BeautifulSoup(start_html.text, 'html.parser')
#     for span in bsObj.find("div", {"class": "content"}).findAll("span"):
#         span_IP=re.findall(r'\d+.\d+.\d+.\d+:\d+', span.text)
#         if IP_Test(span_IP,test_URl):#测试通过
#             IP_list.append(span_IP)
#             print('测试通过，IP地址为'+str(span_IP))
#             if len(IP_list)>num_IP-1: #搜集够N个IP地址就行了
#                 print('搜集到'+str(len(IP_list))+'个合格的IP地址')
#                 return IP_list
#     return IP_list
IPS_list = [
    '118.123.245.206:80',
    '58.221.75.7:8888',
    '58.68.226.186:80',
    '58.221.75.145:8888',
    '210.72.95.134:80',
    '117.36.73.83:80',
    '117.34.47.7:8888',
    '210.22.180.94:80',
    '111.13.65.251:80',
    '210.22.77.78:80'
     
]
def get_image_header():#获取随机的header
    return {'User-Agent': random.choice(UserAgent_List),
             'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
             # 'Host': 'pics.dmm.co.jp',
             'Cache-Control': 'no-cache',
             'Upgrade-Insecure-Requests': '1',
             # 'Referer': 'http://f3.1024xv.com/pw/htm_data/22/1611/486610.html'
             }            
# IP_list=get_IPlist(URL_IP)
def get_random_IP():#随机获取一个IP
#     ind = random.randint(0, len(IP_list)-1)
    ind = random.randint(0, len(IPS_list)-1)
    return IPS_list[ind][0]            
def download_single_image(image_url,x,filePath,proxy_flag=False,try_time=0):#首先尝试直接下载，一次不成功则尝试使用代理
#     if not proxy_flag:#不使用代理
#         try:
            image_html = requests.get(image_url, headers=get_image_header(), timeout=20)
#             print('图片直接下载成功')
#             time.sleep(3)
#             if image_html and len(image_html.content)<4000:
#                 image_html = requests.get(image_url, headers=get_image_header(), timeout=20)
#                 time.sleep(3)
#                 if image_html and len(image_html.content)<4000:
#                     image_html = requests.get(image_url, headers=get_image_header(),timeout=20)
                    
                    
#                     time.sleep(3)
#                     opener=urllib.request.build_opener()
#                     opener.addheaders=[('User-Agent',random.choice(UserAgent_List))]
#                     opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
#                     urllib.request.install_opener(opener)
#                     urllib.request.urlretrieve(image_url,saveFile(x,image_url,filePath))
#                     print(image_url)
#                     if image_html and len(image_html.content)<4000:
#                     return download_single_image(image_url,x,filePath,proxy_flag=True)#否则调用自己，使用3次IP代理
            return image_html #一次就成功下载！
       
#         except:
#             return download_single_image(image_url,x,filePath, proxy_flag=True)#否则调用自己，使用3次IP代理
#     else:#使用代理时
#         if try_time<3:
#             try:
#                 print('尝试第'+str(try_time+1)+'次使用代理下载'+image_url)
# #                 IP_address=get_random_IP()[0]+
#                
#                 image_html = requests.get(image_url, headers=get_image_header(),timeout=20)
#                 print('状态码为'+str(image_html.status_code))
# #                 if image_html.status_code==200:
#                 if image_html and len(image_html.content)>4000:
#                     print('图片通过IP代理处理成功！')
#                     return image_html  # 代理成功下载！
#                 else:
#                     return download_single_image(image_url,x,filePath, proxy_flag=True, try_time=(try_time + 1))
#             except:
#                 print('IP代理下载失败')
#                 return  download_single_image(image_url,x,filePath, proxy_flag=True, try_time=(try_time+1))  # 否则调用自己，使用3次IP代理
#         else:
#             print('图片未能下载')
            return None
def saveFile(x,path,filePath):
    #设置每个图片的路径
    pos = path.rindex('/')
    t = os.path.join(filePath,x+path[pos+1:])
    return t


def openPage(UrlList):#所有的1页中的要处理的条数
    for pageUlr in UrlList:
        try:
            start_html = requests.get(pageUlr, headers=headers)
            start_html.encoding='utf-8'
          
            bsObj=BeautifulSoup(start_html.text,'html.parser')
            di  = bsObj.select('td.h   ')[0]#多个包含 td.h的也签
#             torrent_link = di.select('#read_tpc > a ')[0].get('href')
            dd= str(get_format_filename(di))
#             Html = utf8_transfer(Html)  
#<td class="h"><b>本页主题:</b> 游客  【无帐号人员】发帖教程 图片之间请留空格 并标注图片数量 [7p]</td>
            z=dd[26:]
            x=z[:-5]
                
            openUrl(pageUlr,x)
        except:
            print('地址：'+pageUlr+'下载失败')
def get_format_filename(input_filename): #文件夹的名字不能含有的特殊符号，windows下的限定
    for s in ['?', '*', '<', '>', '\★', '！']:
        while s in input_filename:
            input_filename = input_filename.strip().replace(s, '')
    return input_filename
#URL = baseUrl+'thread0806.php?fid=16&search=&page=' xiezhen 忍野忍 6页 http://1024.stv919.pw/pw/thread.php?fid=14&page=
#URL = baseUrl+'thread0806.php?fid=16&search=&page=' zipai  http://1024.stv919.pw/pw/thread.php?fid=15
#http://1024.97luhi.me/pw/thread.php?fid=15&page= http://1024.stv919.pw/pw/thread.php?fid=15
URL ='http://1024.stv919.pw/pw/thread.php?fid=15&page='
for num in range(1,1111):
#     print("#######################################")
#     print("##########总目录下载地址#############################")
    print("=====================>"+URL+str(num))
#     print("#######################################")
#     print("#######################################")
    UrlList = getUrl(URL+str(num)) 
    openPage(UrlList)
# start_html = requests.get(URL_1024,  headers=headers)
# start_html.encoding='utf-8'
# bsObj = BeautifulSoup(start_html.text,'html.parser')
# for a in bsObj.find("tbody", {"style":"table-layout:fixed;"}).findAll("a"):
#     if ('href' in a.attrs) and ('title' not in a.attrs ) :
#         if re.match(r'^htm_data/.+.html', a.attrs['href']):
#             a_path = get_format_filename(a.text) #的到连接中文名称
#             if not os.path.exists(os.path.join(file_path, a_path)):
#                 os.makedirs(os.path.join(file_path, a_path))
#             os.chdir(file_path+'\\'+a_path)#切换到上面创建的文件夹
#             f = open(a_path+'.txt', 'w')# r只读，w可写，a追加
#             f.write(get_inner_link(a.attrs['href']))
#             f.close()
#             Process_SubPage(file_path+'\\'+a_path, a.attrs['href'])#处理子页面，包括下载图片，种子
#             print(get_inner_link(a.attrs['href']))
#             print(a_path+'：处理完毕')
#             # time.sleep(0.5)#设置等待还是会被服务器封禁


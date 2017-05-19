'''
Created on 2017年5月16日

@author: master-hadoop
'''

#coding:utf-8
import os
import random
import re
import socket
import time
import urllib

from bs4 import BeautifulSoup
from pip._vendor.distlib.locators import Page
import requests
from setuptools.sandbox import save_path

from proxytest import download_single_image


# from proxytest import download_single_image, UserAgent_List, get_random_IP
#DownPath = 'F:\Python\Python3'
DownPath='C:\meitu\meitu03'
head = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
# head={'User-Agent': random.choice(UserAgent_List),
#        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#              # 'Host': 'pics.dmm.co.jp',
#              'Cache-Control': 'no-cache',
#              'Upgrade-Insecure-Requests': '1'
#       
#       }

TimeOut = 5
PhotoName = 0
c = '.jpeg'
PWD='C:\meitu\meitu03'
for x in range(59,1111): #http://www.meizitu.com/a/174.html

    #sleep_download_time=10
    try: 
#         time.sleep(sleep_download_time)
        site = "http://www.meizitu.com/a/%d.html" %x
        print(site)
        Page = requests.Session().get(site,headers=head,timeout=TimeOut)
        #Page = requests.session().get(site, headers=head, proxies={'http:178.140.102.32:8081' },timeout=20)#get_random_IP()

    #Page = urllib.request.urlopen(site)#这里是要读取内容的url  
    except  UnicodeDecodeError as e :
        print('-----UnicodeDecodeError url:',site)  
    except urllib.error.URLError as e:  
        print("-----urlError url:",site)  
  
    except socket.timeout as e:  
        print("-----socket timout:",site)       
    Coding =  (Page.encoding)
    Content = Page.content#.decode(Coding).encode('utf-8')
    ContentSoup = BeautifulSoup(Content)
    jpg = ContentSoup.find_all('img',{'class':'scrollLoading'})#scrollLoading
    for photo in jpg:
        PhotoAdd = photo.get('src')
        PhotoName +=1
        Name =  (str(PhotoName)+c)
        r = requests.get(PhotoAdd,stream=True)
#         with open(PWD+Name, 'ab') as fd:
#             for chunk in r.iter_content():
#                 fd.write(chunk)
        print(PhotoAdd)
        image=download_single_image(PhotoAdd)  
        if image and len(image.content)>40:  # 如果不是为空，则说明下载到了,另外图片如果太小，说明图片数据错误（全黑的），一般都是网站上这个图确实没数据
            os.chdir(PWD)
            f = open(str(Name), 'ab')
            print('下载得到图片！保存图片'+str(Name)+'大小为'+str(len(image.content)))
            f.write(image.content)
            f.close()    
#         print ("You have down %d photos" %PhotoName)

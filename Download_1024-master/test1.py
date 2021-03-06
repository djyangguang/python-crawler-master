#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import re
import time

from bs4 import BeautifulSoup
import requests  # #导入requests

from zcy_fun import get_format_filename, Process_SubPage
from zcy_fun import get_inner_link


def writerLog(Message):
    looger=logging.getLogger()
    filename =time.strftime('%Y-%m-%d',time.localtime(time.time()))
    handler=logging.FileHandler("F:\\xiezhen\\"+filename+"种子.info")
    looger.addHandler(handler)
    looger.setLevel(logging.INFO)
    looger.info(Message)
file_path_youma='F:\caoliu\Python3'#'D:\MyProjectFile\Python\studyproject\Python3\StudyPro1'#存储的地址
file_path_wuma='F:\caoliu\omei'
headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            'Accept-Encoding':'gzip',
           }#初始使用的header
#种子 13页
URL_1024='http://1024.stv919.pw/pw/thread.php?fid=22?fid=15&page=2' #22有
#http://1024.stv919.pw/pw/thread.php?fid=14&page=7
URL_youma ='http://1024.stv919.pw/pw/thread.php?fid=22&page=' #到了13页
URL_wm ='http://1024.stv919.pw/pw/thread.php?fid=7&page=' #到了13页
for num in range(4,111):      
    start_html = requests.get(URL_wm+str(num),  headers=headers)
    start_html.encoding='utf-8'
    bsObj = BeautifulSoup(start_html.text,'html.parser')
    writerLog(URL_wm+str(num))
    for a in bsObj.find("tbody", {"style":"table-layout:fixed;"}).findAll("a"):
        if ('href' in a.attrs) and ('title' not in a.attrs ) :
            if re.match(r'^htm_data/.+.html', a.attrs['href']):
                a_path = get_format_filename(a.text) #的到连接中文名称
                if not os.path.exists(os.path.join(file_path_wuma, a_path)):
                    os.makedirs(os.path.join(file_path_wuma, a_path))
                    os.chdir(file_path_wuma+'\\'+a_path)#切换到上面创建的文件夹
                    f = open(a_path+'.txt', 'w')# r只读，w可写，a追加
                    f.write(get_inner_link(a.attrs['href']))
                    f.close()
                    Process_SubPage(file_path_wuma+'\\'+a_path, a.attrs['href'])#处理子页面，包括下载图片，种子
#                     print(get_inner_link(a.attrs['href']))
                    
                    print(a_path+'：处理完毕')
            # time.sleep(0.5)#设置等待还是会被服务器封禁

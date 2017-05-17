'''
Created on 2017年5月16日

@author: master-hadoop
'''

#coding:utf-8
import os
import re
import urllib

from bs4 import BeautifulSoup
import requests
from setuptools.sandbox import save_path

from proxytest import download_single_image


#DownPath = 'F:\Python\Python3'
DownPath='D:\MyProjectFile\Python\studyproject\Python3'
head = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
TimeOut = 5
PhotoName = 0
c = '.jpeg'
PWD='D:\MyProjectFile\Python\studyproject\Python3'
for x in range(1,111): #http://www.meizitu.com/a/1.html
    site = "http://www.meizitu.com/a/%d.html" %x
    Page = requests.session().get(site,headers=head,timeout=TimeOut)
    Coding =  (Page.encoding)
    Content = Page.content#.decode(Coding).encode('utf-8')
    ContentSoup = BeautifulSoup(Content)
    jpg = ContentSoup.find_all('img',{'class':'scrollLoading'})#scrollLoading
    for photo in jpg:
        PhotoAdd = photo.get('src')
        PhotoName +=1
        Name =  (str(PhotoName)+c)
        #r = requests.get(PhotoAdd,stream=True)
        #with open(PWD+Name, 'wb') as fd:
            #for chunk in r.iter_content():
                #fd.write(chunk)
        image=download_single_image(PhotoAdd)  
        if image and len(image.content)>40000:  # 如果不是为空，则说明下载到了,另外图片如果太小，说明图片数据错误（全黑的），一般都是网站上这个图确实没数据
            os.chdir(PWD)
            f = open(str(Name), 'ab')
            print('下载得到图片！保存图片'+str(Name)+'大小为'+str(len(image.content)))
            f.write(image.content)
            f.close()    
        print ("You have down %d photos" %PhotoName)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import random
import re
import time

from bs4 import BeautifulSoup
import requests

from proxytest import download_single_image


web_domain = 'http://t3.9laik.rocks/pw/'#这一部分加上子页面的href就是子页面的网址
headers = {
	'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
	'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	'Accept-Encoding': 'gzip',
	}
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

torrent_headers = {
   
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Length':'36',
            'Content-Type':'application/x-www-form-urlencoded',
            'Cookie':'__cfduid=d95f26e681331c5c869f91bd2ab1f91b21495153035; a4184_pages=2; a4184_times=1',
            'Host':'www3.uptorrentfilespacedownhostabc.com',
            'Origin':'http://www3.uptorrentfilespacedownhostabc.com',
            'Referer':'http://www3.uptorrentfilespacedownhostabc.com',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':random.choice(UserAgent_List),
           
    }
#  'User-Agent':random.choice(UserAgent_List),

def get_format_filename(input_filename): #文件夹的名字不能含有的特殊符号，windows下的限定
	for s in ['?', '*', '<', '>', '\★', '！','～',':']:
		while s in input_filename:
			input_filename = input_filename.strip().replace(s, '')
	return input_filename

def get_inner_link(URL_part2, URL_part1=web_domain):  # 返回子页面的URL
	return URL_part1 + URL_part2
def get_torrent(torrent_link, filename):
    	#http://www3.uptorrentfilespacedownhostabc.cloud/updowm/file.php/OPHF62s.html
    print('下载种子！')
    torrent_download_url = 'http://www3.uptorrentfilespacedownhostabc.com/updowm/down.php'#'http://www3.uptorrentfilespacedownhostabc.rocks/updowm/down.php'
# 	torrent_download_url='http://www3.uptorrentfilespacedownhostabc.com/updowm/down.php'
    s = requests.Session()
    wb_date = s.get(torrent_link, headers=headers)
    wb_date.encoding = 'utf-8'
    soup = BeautifulSoup(wb_date.text, 'html.parser')
    data = {}
    for i in soup.select('form input'):
        if i.get('name'):
            data[i.get('name')] = i.get('value')
            # print data
    torrent = s.post(torrent_download_url, headers=torrent_headers, data=data)
    with open(filename+'//'+'ss'+ '.torrent', 'ab') as f:#open(a_path+'.txt', 'w')# r只读，w可写，a追加
      #  print('下载得到图片！保存图片'+str(filename)+'大小为'+str(len(torrent)))
		
		   f.write(torrent.content)
def Process_SubPage(save_path, img_url):
	
	start_html = requests.get(get_inner_link(img_url), headers=headers)#返回Response: <Response [200]>只要不是访问图片，一般都不会被封禁，不用换header和IP
	start_html.encoding = 'utf-8'
	bsObj = BeautifulSoup(start_html.text, 'html.parser') #取到网页数据
	print('子页面读取完毕，开始尝试处理图片')
	urlList = []
	#          if ('href' in a_img.attrs) and ('title' not in a_img.attrs ) :
#          		print(a_img.attrs['href'])
#          if re.match(r'^/updowm/.+.html', a_img.attrs['href']) :
	for a in bsObj.find("div", {"id": "read_tpc"}).findAll("a"):#处理图片
           if ('href' in a.attrs) and ('title' not in a.attrs ) :
            	
               if re.match(re.compile(r'http://www3.uptorrentfilespacedownhostabc'), a.attrs['href']): #这个方法会从符串的开头匹配模式（也就是说字符串从第一个字符开始就需要能够匹配到模式，字符串中间的某些字符能够匹配模式是不行的），如果匹配到会返回 Match 对象，否则返回 None。
                   url2 = a.attrs['href']
                   get_torrent(url2, save_path)
#                    urlList.append(url2)
# 	for a_img in bsObj.find("div", {"id": "read_tpc"}).findAll("a"):#处理图片
# 		if ('href' in a.attrs) and ('title' not in a.attrs ):
#        	 if re.match(r'^htm_data/.+.html', a.attrs['href']):	
# #                    url2 = baseUrl+a.attrs['href']
# 			print(a_img.attrs['href'])
#              urlList.append(a_img.attrs['href'])		
	
	img_ind = 1  # 下标
# 	print(bsObj)
# 	IP = soup.select('div.arc > div.content > p > span')
# 	ii = bsObj.select('div.tpc_content > a > href ')#[0].get('href') 	
# 	IP_lists = []
#     for i in ii:
#       span_IP = i.get_text().encode('utf-8').split('@')[0]
#          	print (span_IP)	
#          	ii.append(span_IP) uptorrentfilespacedownhostabc
# 	for a_img in bsObj.find("div", {"id": "read_tpc"}).findAll("uptorrentfilespacedownhostabc"):#处理图片
# 		if ('src' in a_img.attrs):
# 			print('图片URL为' + a_img.attrs['src'])
# 	print(ii)
# 	get_torrent(ii, save_path)
	
	for a_img in bsObj.find("div", {"id": "read_tpc"}).findAll("img"):#处理图片
		if ('src' in a_img.attrs):
			print('图片URL为' + a_img.attrs['src'])
			image = download_single_image(a_img.attrs['src'])
			#time.sleep(0.3)#停止
			
			if image and len(image.content)>40:  # 如果不是为空，则说明下载到了,另外图片如果太小，说明图片数据错误（全黑的），一般都是网站上这个图确实没数据
				os.chdir(save_path)
				f = open(str(img_ind) + '.jpg', 'ab')
				print('下载得到图片！保存图片'+str(img_ind)+'大小为'+str(len(image.content)))
				f.write(image.content)
				f.close()
			img_ind += 1
	
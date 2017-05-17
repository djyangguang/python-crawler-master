#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import random
import re
import time

from bs4 import BeautifulSoup
import requests

from proxytest import download_single_image, UserAgent_List


web_domain = 'http://t3.9laik.rocks/pw/'#这一部分加上子页面的href就是子页面的网址
headers = {
	'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
	'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	'Accept-Encoding': 'gzip',
	}

torrent_headers = {
   
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Length':'36',
            'Content-Type':'application/x-www-form-urlencoded',
            'Cookie':'__cfduid=da1db3ca93a85468ddad109ef4edf69121494855775; a4184_pages=2; a4184_times=2',
            'Host':'www3.uptorrentfilespacedownhostabc.club',
            'Origin':'http://www3.uptorrentfilespacedownhostabc.club',
            'Referer':'http://www3.uptorrentfilespacedownhostabc.club',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':random.choice(UserAgent_List),
    }

def get_format_filename(input_filename): #文件夹的名字不能含有的特殊符号，windows下的限定
	for s in ['?', '*', '<', '>', '\★', '！']:
		while s in input_filename:
			input_filename = input_filename.strip().replace(s, '')
	return input_filename

def get_inner_link(URL_part2, URL_part1=web_domain):  # 返回子页面的URL
	return URL_part1 + URL_part2
def get_torrent(torrent_link, filename):
    	#http://www3.uptorrentfilespacedownhostabc.cloud/updowm/file.php/OPHF62s.html
    print('下载种子！')
    torrent_download_url = 'http://www3.uptorrentfilespacedownhostabc.rocks/updowm/down.php'
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
	start_html = requests.get(get_inner_link(img_url), headers=headers)#只要不是访问图片，一般都不会被封禁，不用换header和IP
	start_html.encoding = 'utf-8'
	bsObj = BeautifulSoup(start_html.text, 'html.parser')
	print('子页面读取完毕，开始尝试处理图片')
	img_ind = 1  # 下标
	#print(bsObj)
	#torrent_link = bsObj.select('#read_tpc > a')[0].get('href')
	#get_torrent(torrent_link, save_path)
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
	

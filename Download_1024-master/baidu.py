'''
Created on 2017年5月17日

@author: master-hadoop
说明：下载百度图片中的美女图片

修改：默认url都已经写好了，只需要改一下cookies就可食用

附加：运用了多线程，一个线程生产url，十个线程消费下载图片

解释： 
1、用正则表达式解析网页内容 
2、建议用IDE工具运行，以便随时终止 
3、用的os模块，在工作空间里建立一个《小图片》的文件夹，图片都默认下载里面

缺点：我不太懂js的图片瀑布流效果怎么弄，所以一个关键词页面只能下载30张左右图片就转到其他的页面了

注意:这个是简单爬虫，爬完页面会自动爬 网页上面推荐的其他页面，即 相关搜索
'''
import os
import  re
import requests
import threading

#得到路径，建立小图片文件夹，图片默认下载其中
currentpath=os.getcwd()
if not os.path.exists(currentpath+os.sep+'小图片'):
    os.mkdir(currentpath+os.sep+'小图片')

cookies={'xxxxxxxx': 'xxxxxxxx'}#用自己的cookies，别拿我的干坏事

headers={'Host':'xxxxxxxx',#封装头部，否则有些图片下载不下来
'Referer':'xxxxxxxxxxxxx',
'Upgrade-Insecure-Requests':'x',
'User-Agent':'xxxxxxxxxxxxxxxxxxxxxxxxx'}

#得到页面上图片的url与相关搜索的url
def search(searchurl):
    response = requests.get(searchurl,cookies=cookies,headers=headers)
    text=response.text
    s = re.findall(r'thumbURL":"([a-zA-z]+://[\w\.%=/\d,&]*)', text)#所有图片的url
    m = re.findall(r'search/index.(\S*)"', text)#当前页面指向其他页面的url
    return s,m

#根据传入的url与jpg名字下载图片
def download_pic(url,name):
    path=os.getcwd()+os.sep+'小图片'
    data=requests.get(url,cookies=cookies,headers=headers).content
    with open(path+os.sep+name,'wb') as f:
        f.write(data)
    print('图片下载完成：%s' % name)


gimagelist=[]#图片的url
queue=[]#相关搜索的url
queue.append('tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&fm=index&pos=history&word=%E7%BE%8E%E5%A5%B3')#默认搜索关键词美女，你也可以换成其他的关键词url的index?后面的部分
gCondition=threading.Condition()#线程相关
visited=set()#用来存放已经搜过的页面的url
class Producer(threading.Thread):
    def run(self):
        print('%s started' % threading.current_thread())
        global gimagelist
        global gCondition
        global queue
        for j in range(1):#我默认循环一次，你也可以改很多
            a=queue.pop(0)#从队列中取出一个关键词url尾部
            searchurl='http://image.baidu.com/search/index?'+a#封装成url
            if searchurl not in visited:#如果没有访问过
                imgs,otherurl=search(searchurl)

                gCondition.acquire()#上锁
                for i in imgs:
                    gimagelist.append(i)#添加图片url
                gCondition.notify_all()#唤醒所有等待的消费者
                gCondition.release()#释放锁
                visited.add(searchurl)#标记为已访问过
                queue.extend(otherurl)#将相关搜索的url放入



class Consumer(threading.Thread):
    def run(self):
        print('%s started' % threading.current_thread())
        while True:
            global gimagelist
            global gCondition

            gCondition.acquire()#上锁
            while len(gimagelist)==0:
                gCondition.wait()#没有则等待
            url=gimagelist.pop()
            name=url.rsplit('/')[-1]#取名字，以url后面的部分做名字
            gCondition.release()
            download_pic(url,name)#下载图片


if __name__=='__main__':
    Producer().start()

    for i in range(10):#十个消费者线程数
        Consumer().start()
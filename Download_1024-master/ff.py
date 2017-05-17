    # coding:utf8
    '''
    作者: 死猪
    日期: 2017年1月29日
    系统环境: WIN7 X64 其他系统未测试
    脚本: 使用影梭挂本机1080端口做代理,访问1024网站抓取最新图片和种子保存在本地
    因为亚洲无码区赌博广告太多提取麻烦,目前只做了动漫区的
    因为考虑到种子的时效问题,所以只下载第一页的,也就是当天更新的内容,不过也不少了,每天大概都会更新30个左右
    第一页有接近100个帖子,就是说第一次运行会下载接近100个
    之后会只下载更新的,其他的会根据目录中的情况判断下载
    注意: 该脚本依托于能开启内网端口代理共享的梯子软件才能正常访问目标网站
    '''
    import re 
    import shutil 
    import os 
    import requests
    import threading

    # 主函数: 访问列表页并解析页面中可访问的帖子地址
    def main(url):
        try:
            r = s.get(url, proxies=本机代理)
        except Exception as e:
            print("网络故障,请检查网络环境(比如开影梭之类的)")
            return
        # 首先要粗略的提取一次
        onepassHtml = re.search('普通([\s\S])+&gt;&gt; BT', r.content.decode("gbk", "ignore"))
        # 然后再细提一次,这样就把置顶的帖子略过了
        urllsit_r = re.findall('&lt;h3&gt;.+&lt;/h3&gt;', onepassHtml.group())

        urllist = dict() # 建立一个字典用来保存分区里面帖子列表
        for i in urllsit_r:
            p = re.compile('"(.+?)".*&gt;(.+?)&lt;+')
            x = p.search(i)
            # x.group(1) 抓取到的地址用来做键值 x.group(2) 帖子的名字用来做键名
            urllist[x.group(2)] = x.group(1)

        # urllist.keys() 键值(地址)
        # urllist.values() 键名(文件名)
        # urllist.items() 两者皆有

        for i,j in urllist.items():
            # 往线程池里面添加线程对象
            threads.append(threading.Thread(target = 解析帖子页面, args = ("http://t66y.com/" + j, i)))
            # 启动线程池
        for t in threads:
            t.start()
            # 等待线程池所有线程退出
        for t in threads:
            t.join()

        print("所有任务完成")
    # 该函数负责创建目录,解析页面,调用图片遐和种子下载函数
    # 该函数属于线程函数,因为没有公共资源,没有添加线程锁和排序模块
    def 解析帖子页面(帖子地址, 下载目录):
        # windows目录名字中不能包含 \/*?|:&lt;&gt; 这几个符号,所以把他们全部替换成 ★ 避免WINdows系统报错
        下载目录, 匹配到的数量 = re.subn('[\\/*?|:&lt;&gt;]', "★", 下载目录) 
        # 1. 新建目录,目录名字是获取到的帖子名字
        try:
            os.mkdir(下载目录)
        except WindowsError as e:
            print("已存在该种子,放弃下载...")
            return False

        # 现在有了一个不错的目录
        # 我们给垃圾网络三次机会载入帖子,如果没有载入的话,后面也无从说起了

        for i in range(3):
            楼主帖子内容 = 图片及种子地址分析(帖子地址)
            if 楼主帖子内容:
                break
        if 楼主帖子内容 == None:
            print("重试三次无法打开帖子,解析失败...")
            return

        # 2. 在相应位子匹配图片并下载到新建目录中
        # &lt;img src='(.+)' onclick 得到图片
        图片地址 = re.search(r"&lt;img src='(.+)' onclick", 楼主帖子内容)
        print("正在下载图片 %s" % (图片地址.group(1)))
        # 尝试下载三次图片,三次后还是无法下载,就承认失败
        for i in range(3):
            if 下载图片(图片地址.group(1), 下载目录 + "/01.jpg"):
                break
        # 3. 解析种子地址,访问并下载种子到新建目录 &gt;http://(.+)&lt;/a 得到种子网址
        种子下载页面地址 = re.search(r"&gt;http://(.+)&lt;/a", 楼主帖子内容)
        # 调用下载种子函数,下载到指定目录, 三次机会连续下载
        print("正在下载种子 %s" % (种子下载页面地址.group(1)))
        for i in range(3):
            if 下载种子("http://" + 种子下载页面地址.group(1),下载目录):
                break

        return True

    #根据读取到的页面分析具体地址,返回成功与否
    def 图片及种子地址分析(帖子地址): 

        r = s.get(帖子地址, proxies=本机代理)
        try:
            帖子重点数据区域 = re.search('h4&gt;([\s\S]+)主]&lt;/a&gt;', r.content.decode("gbk", "ignore"))
            return 帖子重点数据区域.group(1)
        except Exception as e:
            return None

    def 下载图片(下载网址, 图片文件):
        r = s.get(下载网址, stream=True, proxies=本机代理)
        # 如果网站返回头代码是200 代表连接成功,获取数据流
        if r.status_code == 200:
            with open(图片文件, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

        if os.path.exists(图片文件):
            return True
        else: 
            return False

    def 下载种子(下载网址, 下载目录):
        # (1) 访问种子页面
        r = s2.get(下载网址, proxies=本机代理)
        # (2) 获取页面中按钮的reff值
        # 注意,该网站编码不是gb2312 而是utf8
        reff = re.search('"([A-Za-z0-9]{14})=', r.content.decode("utf8", "ignore"))
        ref = re.search('([0-9a-z]{40,45})', r.content.decode("utf8", "ignore"))
        submit = re.search('ue=(\w+)', r.content.decode("utf8", "ignore"))
        # (3) 拼接点击下载按钮链
        下载页面主机地址 = re.search('//(.+)/', 下载网址)
        下载按钮链接 = "http://" + 下载页面主机地址.group(1) + "/download.php?ref=" + ref.group(1) + "&amp;reff=" + reff.group(1) + "%3D%3D&amp;submit=" + submit.group(1)
        print("已获取种子下载真实地址...")
        # 使用流模式访问该地址
        r = s2.get(下载按钮链接, stream=True, proxies=本机代理)
        种子文件 = 下载目录 + "/种子.torrent"
        # 如果网站返回头代码是200 代表连接成功,获取数据流
        if r.status_code == 200:
            with open(种子文件, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

        # 检查种子是否下载成功,并返回结果
        if os.path.exists(种子文件):
            return True
        else: 
            return False

    if __name__ == '__main__':
        # 设置代理为本机SSR端口,这个网站不翻墙还是看不了的
        本机代理 = { "http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080", }
        # 访问1024网站专用对象
        s = requests.session() 
        # 访问种子站专用对象,因为网站不同,所以用单独的对象处理cookie和session
        s2 = requests.session() 
        # 线程池
        threads = list()
        # 开启运行,目标是动漫区
        main("http://t66y.com/thread0806.php?fid=5") 

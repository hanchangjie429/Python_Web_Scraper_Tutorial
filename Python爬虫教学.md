这几天在帮经理做一些爬取数据的任务，借由这个机会，来写一篇有关python爬虫的文章，一是希望能够跟大家分享一些学习的经验，二来也是为了巩固一下自己的知识。

## 一. 爬虫主要用到的package库
- requests（第一当之无愧）
- bs4 分析源代码
- pandas 处理数据
- time 设置爬取时间间隔
- lxml xpath方法
- pretty_errors (美化异常信息，能够让你更清晰更直观的找出错误信息)


## 二. 网页解析
当我们想要爬取某个网站的时候，我们首先要将这个网页的源代码获取下来，因为源代码是网页信息的载体，有了网页源代码之后我们才能从网页中获取我们需要的信息。
那么，如何获取我们的网页源代码呢？

一个很简单的第三方库可以帮到你，他就是**requests**，例如，我们想要获取豆瓣的源代码，首先我们要对豆瓣网页发起请求，这个动作我们可以通过requests.get来完成。
```python
import requests

url = 'http://www.douban.com'
response = requests.get(url)
print(response)
```

这时，可以看到我们的终端输出

```python
<Response [418]>
[Finished in 1.5s]
```

我们收到了一串数字，418。这其实是在说明，我们的请求被拒绝访问，返回码418是I'm a teapot。 [详情可以查看这个链接](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/418)

[有关其他的返回码可以查看这个文档](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

为什么我们的请求会被拒绝访问呢，这是因为，我们在访问豆瓣的时候，豆瓣的服务器检测到我们在使用机器访问，用户访问和机器访问的区别就在于header头文件信息，我们在手动访问豆瓣的时候，我们的请求会带上我们的用户头文件信息。因此在我们用机器访问的时候，带上我们的用户头文件信息，就能够模拟用户来对页面进行访问。

在这里，我们添加我们的头文件信息至我们的requests里面，
```python
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
response = requests.get(url,headers=headers)
print(response)

```

现在我们可以发现，这时的返回码是200,意思就是访问成功，得到了服务器的回复
```python
<Response [200]>
[Finished in 1.7s]
```

如果我们此时想要得到豆瓣页面的源代码，可以使用.text方法
```
print(response.text)
```

输出：
```HTML
...
<html lang="zh-CN" class="ua-windows ua-webkit">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="renderer" content="webkit">
    <meta name="referrer" content="always">
    <meta name="google-site-verification" content="ok0wCgT20tBBgo9_zat2iAcimtN4Ftf5ccsh092Xeyw" />
    <title>
豆瓣电影 Top 250
</title>
    
    <meta name="baidu-site-verification" content="cZdR4xxR7RxmM4zE" />
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="Sun, 6 Mar 2005 01:00:00 GMT">
...
```
这样，我们就成功爬取了豆瓣的网页源代码


## 三. 反爬虫

由于在我们爬取网页信息的过程中，随着技术的发展，我们所访问的服务器会对爬虫进行一系列的检测，通过各种方式阻止我们使用爬虫获取相关的数据，所以各种反爬技术也应运而生。这一小节我们重点将一些反爬虫的内容。

### 1. 头部信息（user-agent/referer）
最直接的反爬方法就是在我们进行网页请求的时候，就带上我们访问的头部信息。具体每个网站所需要的头部信息我们得在网页内部使用调试模式（F12）之后，在network标签里的request header里面获知。但是模拟人类浏览行为所需的最基本的头部信息包括user-agent用户代理，referer网页来源。
user-agent

#### 1) User-Agent
什么是User-Agent?
User-Agent中文名为用户代理，简称 UA，是Http协议中的一部分，属于头域的组成部分，它是一个特殊字符串头，使得服务器能够识别客户使用的操作系统及版本、CPU 类型、浏览器及版本、浏览器渲染引擎、浏览器语言、浏览器插件等。在网络请求当中，User-Agent 是标明身份的一种标识，通过这个标识，用户所访问的网站可以显示不同的排版从而为用户提供更好的体验或者进行信息统计；例如用手机访问谷歌和电脑访问是不一样的，这些是谷歌根据访问者的UA来判断的。UA可以进行伪装。

User-Agent的作用：用来识别是否爬虫.
User-Agent值是用来帮助服务器识别用户使用的操作系统、浏览器、浏览器版本等等信息的，因此也常被用来检测爬虫。许多网站会ban掉来自爬虫的请求，来达到反爬的目的。

```python
正常浏览器的User-Agent值为：Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0
使用requests时的默认User-Agent为：python-requests/2.18.4
scrapy的默认值为：Scrapy/1.5.0 (+https://scrapy.org)
服务器可以轻易识别出该请求是否来自爬虫。因此为了减小爬虫被ban的几率，我们可以通过设置请求的User-Agent来达到欺骗服务器的目的。
```
#### 2) Referer
Referer字面意思是引用，意思就是我们这个页面是从哪个页面跳转过来的，服务器会根据这个字段判断我们是点击跳转访问还是机器get访问。如果我们不在头文件中添加这个字段，就会对我们的爬虫进行限制。我本人也亲自遇到过没有填写referer，然后服务器不停的给我们重定向至其他页面的操作。因此，在header里面添加referer能让我们的爬虫更好的模拟我们的人为操作。


### 2. cookies验证

有的时候我们需要爬取的页面需要用户登陆之后才能够访问，这个时候，cookies就派上了用场。cookies是一种本地缓存，他能够将我们的用户信息在一定的时间内存储在我们的电脑里面，以便我们下次访问的时候可以跳过登陆过程直接进行访问。那么一旦在发起请求的时候带上了我们之前保存的cookies，我们就能够避免用户登陆操作对我们进行的限制。

### 3. selenium、webdriver模拟登陆

webdriver是一个能够模拟用户操作浏览器界面的辅助工具，它可以模拟用户点击，滑动浏览器等一系列操作。

下面的代码用来模拟登陆豆瓣
```python
from selenium import webdriver # 导入webdriver

try:
	browser = webdriver.Chrome() # 新建webdriver对象
	browser.get('http://www.douban.com') # 打开豆瓣主页
	browser.switch_to.frame(browser.find_elements_by_tag_name('iframe')[0]) # 切换iframe至用户名以及密码输入框
	btm1 = browser.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]') # 从“短信登陆/注册”切换至“密码登陆”
	btm1.click() # 模拟点击“密码登陆”按钮

	username = browser.find_element_by_xpath('//*[@id="username"]') # 找到用户名输入框
	username.send_keys('testtesttest') # 传入数据，将testtesttest替换成自己的用户名

	password = browser.find_element_by_xpath('//*[@id="password"]') # 找到密码输入框
	password.send_keys('testtesttest') # 传入数据，将testtesttest替换成自己的密码

	login = browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[5]/a') # 定位“登陆豆瓣”按钮
	login.click() # 点击“登陆豆瓣”按钮

	cookies = browser.get_cookies()
	print(cookies) # 获取登陆之后的cookies

	time.sleep(3) # 进入休息状态，时间间隔3秒钟

except Exception as e:
	print(e) # 异常检测

finally:
	browser.close()
```

webdriver模拟登陆石墨文档
```python

from selenium import webdriver
import pyautogui

try:
	browser = webdriver.Chrome() # 新建webdriver对象
	browser.get('https://shimo.im/welcome') # 打开石墨文档主页

	input_email = pyautogui.prompt(text='请输入邮箱',title='邮箱',default='') # 自定义输入框 输入用户名（email）
	input_password = pyautogui.password(text='请输入密码',title='密码',default='',mask='*') #自定义输入框 输入密码

	item1 = browser.find_element_by_xpath('//*[@id="homepage-header"]/nav/div[3]/a[2]/button') # 定位至“登陆按钮”
	item1.click()

	email = browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div/input')
	email.send_keys(f'{input_email}') # 将刚才输入的用户名传入输入框

	password = browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/input')
	password.send_keys(f'{input_password}') # 将刚才输入的密码传入输入框

	login = browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/button')
	login.click() # 点击登陆

	time.sleep(3)

	browser.get('https://shimo.im/profile') # 跳转至个人简介
	print('finished') # 打印”finished“

except Exception as e:
	print(e)

finally:
	browser.close()
```

### 4. 验证码识别
本文只介绍验证码为字母或者中文的情况下，如何去进行处理，其他的验证手段，请查阅其他资料。

### 5. 代理ip





## 四. 获取数据
beautifulsoup
xpath

## 五. 整理数据
pandas

## 六. 异常处理
try
except

## 七. 数据输出
to_csv
mysql



2020/8/7
---
今天在写爬虫的时候遇到了一个问题，就是当你爬取的数据在某个页面不存在时（比如说page1，page2，page3都有<地址>这个数据，但是page4这个数据缺省了）这个时候你该如何进行异常处理？这个问题我一会儿再来讲。
解决方法：使用try，except进行异常处理，前提是我们的父类结点要具有相同的结构，因为只有这样，才能在某个父节点下出现缺省值的时候返回NoneType错误，这时我们就可以用try，except捕获异常了

2020/8/11
---
今天在写mysql query的时候，我想在python环境下一次性delete多条records，但是每次写的query都显示syntax error，比如我想一次性删除id从19到29的records，我一开始写的code是：

```python
data = [i for i in range(19,30)]
curB.executemany('delete from test_tbl where id=%s',data)
```
我搞不明白为什么这样会出错，一开始我以为是字符格式化的问题，后来才明白，我们使用%s的时候，需要使用元组将不同的数据用逗号隔开，像下面这样
```python
data = [(i,) for i in range(19,30)]
curB.executemany('delete from test_tbl where id=%s',data)
```
这样就能一次性删除多条records了。[参考文章](https://pynative.com/python-mysql-delete-data/)
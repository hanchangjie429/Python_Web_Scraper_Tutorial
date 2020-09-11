# Python_Web_Scraper_Tutorial
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
当我们拿到了我们想要爬取的网页的源代码的时候，再获取我们想要的数据，就变得非常简单了。就像是查找功能一样，python的beautifulsoup以及xpath包都有相应的字段匹配查找功能帮助我们获取我们想要的数据。
1. beautifulsoup的使用方法
```python
from bs4 import BeautifulSoup

soup = beautifulsoup(response.text,'html.parser')

soup.find()

sou.find_all()

```

2. xpath

3. json

## 五. 整理数据
pandas

## 六. 异常处理
try
except
 
## 七. 数据存储
当我们爬取到了我们需要的数据之后，接下来的问题就变成了我们该如何存储这些数据，在哪里存储这些数据，以什么形式存储这些数据。因为我们从网站上抓取的数据一般都是结构化的数据或者json类的数据，因此我们可以以csv的格式以文件的形式存储或者使用关系型数据库来存储我们爬取的数据，在这里我给大家介绍如何用pymysql来连接本地mysql数据库。至于为什么要使用pymysql连接mysql数据库然后在进行操作，而不是直接在mysql中进行操作，是因为我们在python中进行query操作时，可以利用python的循环来进行多条query的执行，为我们的insert，update等操作节省大量的时间。

首先第一步就是在终端使用pip install pymysql在我们的python目录下安装pymysql的package，安装完成后，我们就可以开始在python中进行数据库的关联操作
```python
import pymysql

# 在这里完善自己的mysql数据库配置
db_config = {
	'host':'localhost',
	'user':'root',
	'password':'******',# 使用自己的密码
	'db':'db_test'.
	'port':3306
}
# 建立与mysql的连接，将db_config配置参数传入
conn = pymysql.connect(**db_config)

# 建立连接后，就可以新建游标，开始curd（create，update，retrieve，delete）操作了

cur = conn.cursor()
# 在这里输入你的sql_query
sql_query = 'select * from positions limit 10;'

# 下面的代码执行query操作，但是不会在命令行打印出结果
cur.execuete(sql_query)

# 使用fetch函数将执行结果存储在result变量里面，包括fetchone, fetchall,fetchmany
result1 = cur.fetchall()
result2 = cur.fetchone()
result3 = cur.fetchmany(5)

# 打印数据
print(result1,result2,result3)
```
这就是最简单的使用pymysql连接mysql数据库，并从中查询数据的流程，存储数据的流程跟查询差不多，主要区别在于我们的query要先创建表，然后再把我们的数据insert到我们的表中就好了，可能比较需要注意的操作就是如何使用python的循环功能+mysql的insert语句，快速往表单中存储元素。

```python
data = ((1, 'title1', 'author1'), (2, 'title2', 'author2'), (3, 'title3', 'author3'), (4, 'title4', 'author4'), (5, 'title5', 'author5'))

比如，我想创建一个叫做test_tbl的表，并把上述records插入进我的表中，我们该如何执行呢？

首先我们得使用create创建一个新的表，并定义好表的字段以及属性。
create table test_tbl2 (
	id int(6) auto_increment primary key,
	title varchar(30) not null,
	author varchar(30) not null)

然后用insert函数+循环将我们的data插入表中
sql_query = 'insert into test_tbl2 (id, title, author) values(%s, %s, %s) '
for i in data:
	cur.execuete(sql_query,i)
# 也可以使用executemany语句一次进行多条语句
# cur.executemany(sql_query,data)

```
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

2020/8/25
---
今天在写爬虫的时候，看到了一个需要post方法请求的网址，但是用f12分析发现这个post方法没有form data，取而代之的是一个叫做request payload的表单信息。这里出现了跟以往post传入数据不一样的形式，之前我们在使用post的时候，传入的是data参数，但是这里request payload 我们需要传入json参数，并把request payload里面的变量以字典形式保存。
[参考文章](https://stackoverflow.com/questions/59726277/post-request-payload-in-python)
[参考文章2](https://stackoverflow.com/questions/23118249/whats-the-difference-between-request-payload-vs-form-data-as-seen-in-chrome#:~:text=The%20Request%20Payload%20%2D%20or%20to,CRLF%20of%20a%20HTTP%20Request.&text=If%20you%20submit%20this%20per,is%20submitting%20as%20payload%20body)

2020/9/3
---
cmind-
1. 用get json方法获取yahoo finance的 financial data
2. 用post json方法获取us public company list


2020/9/4
---
cmind-
1. 用selenium实现yahoo finance自动登陆
2. 带cookies进行requests请求 获取yahoo finance premium的数据


2020/9/7
---
cmind-
1. 利用browser.get_cookies()并将cookie list转为cookie_dict实现selenium自动获取cookie并存储
2. 利用while循环+time.sleep()实现selenium等待验证结束跳转页面


2020/9/8
---
cmind-
1. 结构化数据，data cleaning，提取2018，2019，2020 quaterly数据，填补null值
2. 输出6000+ stock financial files as csv file


2020/9/9
---
cmind-
对昨天的代码进行修改
1. 保留所有变量，不需要提前进行数据预处理，不需要删除变量
2. download 3个financial statements(income_statement,cash_flow,balance_sheet)


2020/9/10
---
cmind-
增加需求
1. 输出json file作为源数据以备之后数据回溯使用
2. json.dump() vs json.dumps()
3. 学习mongodb相关知识
4. 增加 预计完成时间 功能


2020/9/11
---
cmind-
1. 上传json file到drive raw data文件夹
2. 近期成果展示
3. 准备字节面试

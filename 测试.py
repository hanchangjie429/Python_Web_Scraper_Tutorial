import requests
from bs4 import BeautifulSoup
from lxml import etree
import pretty_errors
import time
from fake_useragent import UserAgent


# url = 'https://movie.douban.com/top250'
# headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
# response = requests.get(url,headers=headers)
# print(response.cookies)
# print(response.request.headers)
# print(response.headers)
# print(response.request._cookies)
# print(response.cookies)
# print(response.status_code)
# print(response.text[:100])
# print(response.content[:100])



'''request模拟登录豆瓣
ua = UserAgent(verify_ssl=False)

headers = {
'User-Agent': f'{ua.random}',
'Referer':'https://accounts.douban.com/passport/login?source=movie',
'Host':'accounts.douban.com'
}

login_url = 'https://accounts.douban.com/j/mobile/login/basic'

form_data = {
	'ck': '',
	'name':'13581278612',
	'password':'hcjHCJ123',
	'remember':'false',
	'ticket': ''
}

s = requests.Session()

response = s.post(login_url,headers=headers,data=form_data)
print(response.text)

response2 = s.get('https://accounts.douban.com/passport/setting',headers=headers,cookies=s.cookies)
print(response2)

response3 = s.get('https://www.douban.com/people/121550733/',headers=headers,cookies=s.cookies)
print(response3)
'''



'''随机选择用户代理
from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False)
headers2={}
headers2['User-Agent'] = ua.random
headers2['referer'] = 'www.douban.com'
print(headers2)
response = requests.get('http://www.douban.com')
print(response.request.headers['user-agent'])
'''


'''webdriver模拟登陆豆瓣
from selenium import webdriver
try:
	browser = webdriver.Chrome()
	browser.get('http://www.douban.com')
	browser.switch_to.frame(browser.find_elements_by_tag_name('iframe')[0])
	btm1 = browser.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]')
	btm1.click()

	username = browser.find_element_by_xpath('//*[@id="username"]')
	username.send_keys('13581278612')
	password = browser.find_element_by_xpath('//*[@id="password"]')
	password.send_keys('hcjHCJ123')

	login = browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[5]/a')
	login.click()

	#browser.find_element_by_xpath('//*[@id="db-nav-sns"]/div/div/div[3]/ul/li[2]/a')
	cookies = browser.get_cookies()
	print(cookies)
	time.sleep(3)

except Exception as e:
	print(e)

finally:
	browser.close()
'''



# webdriver模拟登陆石墨文档
from selenium import webdriver
import pyautogui

browser = webdriver.Chrome()
browser.get('https://shimo.im/welcome')

input_email = pyautogui.prompt(text='请输入邮箱',title='邮箱',default='')
input_password = pyautogui.password(text='请输入密码',title='密码',default='',mask='*')

item1 = browser.find_element_by_xpath('//*[@id="homepage-header"]/nav/div[3]/a[2]/button')
item1.click()

email = browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div/input')
email.send_keys(f'{input_email}')

password = browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/input')
password.send_keys(f'{input_password}')

login = browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/button')
login.click()

time.sleep(3)

browser.get('https://shimo.im/profile')

print('finished')





'''webdriver模拟登陆石墨文档
from selenium import webdriver

class ShimoLogin:
	def __init__(self):
		self.home_url = 'https://shimo.im'
		self.profile_url = 'https://shimo.im/profile'
		self.browser = webdriver.Chrome()

	def run(self):
		self.browser.get(self.home_url)

		login_botton = self.browser.find_element_by_xpath('//*[@id="homepage-header"]/nav/div[3]/a[2]/button')
		login_botton.click() # 打开登陆界面

		email = self.browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div/input')
		email.send_keys('testtest')

		password = self.browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/input')
		password.send_keys('testtest')

		login = self.browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/button')
		login.click()

		time.sleep(5)

		self.browser.get(self.profile_url)


def main():
	login_to_shimo = ShimoLogin()
	login_to_shimo.run()

if __name__ == '__main__':
	main()
'''
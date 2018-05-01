import requests
from selenium import webdriver
import time

qq = '974986913'
pwd = '1qaz2wsx'

driver = webdriver.Chrome(executable_path="/Users/ken/Desktop/python Crawler/chromedriver")
# driver.maximize_window()


def get_info(qq):
	
	driver.get('https://user.qzone.qq.com/974986913')
	time.sleep(5)

	print("==========start================")
	try:
		driver.find_element_by_id('login_div')
		a = True
	except:
		a = False
	if a == True:
		print("start simulated login process")
		driver.switch_to.frame('login_frame')
		driver.find_element_by_id('switcher_plogin').click()
		driver.find_element_by_id('u').clear()#选择用户名框
		driver.find_element_by_id('u').send_keys(qq)
		driver.find_element_by_id('p').clear()
		driver.find_element_by_id('p').send_keys(pwd)
		driver.find_element_by_id('login_button').click()
		time.sleep(3)
	driver.implicitly_wait(3)
	# try:
	# 	driver.find_element_by_id('QM_OwnerInfo_Icon')
	# 	b = True
	# except:
	# 	b = False
	# if b == True:
	# 	driver.switch_to.frame('app_canvas_frame')
	# 	content = driver.find_elements_by_css_selector('.content')
	# 	stime = driver.find_elements_by_css_selector('.c_tx.c_tx3.goDetail')
	# 	for con,sti in zip(content,stime):
	# 		data = {
	# 		'time':sti.text,
	# 		'shuos':con.text
	# 		}
	# 		print(data)
	# 	pages = driver.page_source
	# 	soup = BeautifulSoup(pages,'lxml')

	# cookie = driver.get_cookies()
	# cookie_dict = []
	# # for c in cookie:
	# # 	ck = "{0}={1};".format(c['name'],c['value'])
	# # 	cookie_dict.append(ck)
	# # i = ''
	# # for c in cookie_dict:
	# # 	i += c
	# print('Cookies:',i)
	print("==========done================")

	element = driver.find_element_by_id("feed_friend")
	print(element.text)

	

	driver.close()
	driver.quit()

if __name__ == '__main__':
	get_info('974986913')










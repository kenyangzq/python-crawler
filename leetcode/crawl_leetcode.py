import os
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from io import BytesIO
import pandas as pd

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import utils
from reportlab.lib.units import cm
import reportlab.platypus as pypus



class SpiderSelenium(object):
	def __init__(self, usn, pwd):
		self.driver = webdriver.Firefox(executable_path="/Users/ken/Desktop/python Crawler/geckodriver")
		self.driver.maximize_window()

		self.usn = usn
		self.pwd = pwd
		self.problems = []

		# self.soup = BeautifulSoup(self.driver.page_source,'lxml')
		print('webdriver start init success!')

	def __del__(self):
		try:
			self.driver.close()
			self.driver.quit()
			print('webdriver close and quit success!')
		except:
			pass

	# def _need_login(self):
	#     '''
	#     check whether need to sign in
	#     '''
	#     try:
	#         self.driver.find_element_by_link_text('Sign in')
	#         return True
	#     except:
	#         return False

	def _login(self):
		'''
		login to leetcode
		return true if suceed
		return false otherwise
		'''
		
		self.driver.find_element_by_id('id_login').clear()
		self.driver.find_element_by_id('id_login').send_keys(self.usn)
		self.driver.find_element_by_id('id_password').clear()
		self.driver.find_element_by_id('id_password').send_keys(self.pwd)
		self.driver.find_element_by_xpath("//button[@type='submit']").click()

		time.sleep(3)

		avatar = self.driver.find_elements_by_xpath("//img[@class='avatar']")
		return len(avatar) != 0


	def _auto_scroll_to_bottom(self):
		'''
		将当前页面滑动到最底端
		'''
		js = "var q=document.body.scrollTop=10000"
		self.driver.execute_script(js)
		time.sleep(6)



	def _get_problems(self):
		try:
			self.driver.find_element_by_link_text("Problems").click()
		except:
			print("Cannot find \'Problem\'. Something is wrong")
			return 

		time.sleep(5)
		
		## select all problems
		select = Select(self.driver.find_element_by_xpath("//select[@class='form-control']"))
		select.select_by_visible_text('100')
		time.sleep(2)


		problem_table = self.driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div[2]/table")
		tables = problem_table.text.split('\n')[1:-6]
		entrynum = int(len(tables) / 3)

		print("Total problem number: ", str(entrynum))

		directory = './problem_screenshot/'

		if os.path.exists(directory) is False:
			os.makedirs(directory)

		## create the problem table
		## this will take a while
		for i in range(entrynum):
			index = i * 3

			tmp = [tables[index+1].rstrip()]
			if tmp[0][-3:] == "New":
				tmp[0] = tmp[0][:-3].rstrip()
			tmp.append(tables[index+2].split(' ')[1])

			try:
				entry = self.driver.find_element_by_link_text(tmp[0])
			except:
				time.sleep(5)
				entry = self.driver.find_element_by_link_text(tmp[0])

			## get description
			entry.click()
			time.sleep(1)

			## check premium
			try:
				qd = self.driver.find_element_by_xpath("//div[@class='question-description']")
				tmp.append(qd.text)

				im = Image.open(BytesIO(qd.screenshot_as_png))

				filename = directory + 'problem' + str(i+1) + '.png'
				im.save(filename)

			except:
				print("Premium problem: " + str(i + 1))
				tmp.append('Locked')
				

			## get screenshot
			
			time.sleep(1)

			self.driver.back()
			time.sleep(1)

			self.problems.append(tmp)


	def _write_pdf(self):
		'''
		write the problems and screenshot into a pdf file
		'''
		doc = SimpleDocTemplate("Leetcode_Problems.pdf",pagesize=letter,
			rightMargin=72,leftMargin=72,
			topMargin=72,bottomMargin=18)
		styles=getSampleStyleSheet()    	

		difficulty = ParagraphStyle('parrafos',alignment = TA_JUSTIFY,
			fontSize = 8,fontName="Times-Roman",)

		directory = './problem_screenshot/'

		Content = []

		for i in range(len(self.problems)):
			Content.append(Paragraph(str(i+1) + "\t" + self.problems[i][0], styles["Normal"]))
			Content.append(Paragraph(self.problems[i][1], difficulty))

			Content.append(Spacer(1, 12))

			if self.problems[i][2] == 'Locked':
				Content.append(Paragraph('This problem requires premium account.'), styles["Normal"])
			else:
				imagename = directory + 'problem' + str(i+1) +'.png'
				Content.append(self.get_image(imagename, width=16*cm))

			Content.append(Spacer(1, 50))

		doc.build(Content)



	def get_image(self, path, width=1*cm):
		img = utils.ImageReader(path)
		iw, ih = img.getSize()
		aspect = ih / float(iw)
		return pypus.Image(path, width=width, height=(width * aspect))



	def crawl(self):

		self.driver.get('https://leetcode.com/accounts/login/')
		self.driver.implicitly_wait(5)
			
		if self._login():
			print("atomatic login suceeded!")
			
			self._get_problems()
			print("webdriver crawl finish!")

			print("\nnow creating the pdf file")
			self._write_pdf()
			print("pdf file successfully created")
		else:
			print('login failed')
		



if __name__ == '__main__':
	crawler = SpiderSelenium("username", 'password')
	crawler.crawl()

	df = pd.DataFrame(crawler.problems)
	df.to_csv("leetcode_problem.csv")




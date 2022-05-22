import pandas as pd
import time
import re
import os
import csv
import json
from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def buildWebDriver():
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_experimental_option("useAutomationExtension", False)
	chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
	chrome_options.add_argument("user-data-dir=C:/Users/marco/Desktop/FoxyByte/Crawler/Profile") #edit 
	
	driver = webdriver.Chrome("C:/Users/marco/Desktop/FoxyByte/Crawler/chromedriver.exe", options=chrome_options) #edit

	return driver



def getLocationPageBySearchBar(locationName, driver):
#	chrome_options = webdriver.ChromeOptions()
#	chrome_options.add_experimental_option("useAutomationExtension", False)
#	chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#	chrome_options.add_argument("user-data-dir=C:/Users/marco/Desktop/FoxyByte/Crawler/Profile"); #edit 
	
#	driver = webdriver.Chrome("C:/Users/marco/Desktop/FoxyByte/Crawler/chromedriver.exe", options=chrome_options) #edit
	#print("done1")
	driver.get("https://www.instagram.com/")
	#print("done2")
	time.sleep(10)
	#driver.find_elements_by_xpath(".XTCLo d_djL DljaH").send_keys("prova")
	#input_search = wait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@class,'XTCLo')]")))

	element = WebDriverWait(driver, 20).until(
	EC.element_to_be_clickable((By.XPATH, "//input[contains(@class,'XTCLo')]")))

	# error: selenium.common.exceptions.ElementClickInterceptedException: Message: element click intercepted: Element <input aria-label="Input di ricerca" autocapitalize="none" class="XTCLo  d_djL  DljaH " placeholder="Cerca" type="text" value=""> is not clickable at point (518, 30). Other element would receive the click: <div class="eyXLr">...</div>
 
	time.sleep(5)
	#print("waited")
	driver.execute_script("arguments[0].click();", element)

	time.sleep(5)
	element.send_keys(locationName)
	time.sleep(2)

	url_array = driver.find_elements_by_css_selector(".-qQT3")
	
	for url in url_array:
		if 'explore/locations' in str(url.get_attribute('href')):
			print(url.get_attribute('href'))	
			return str(url.get_attribute('href'))




def crawlLocation(locationURL, driver):
	#chrome_options = webdriver.ChromeOptions()
	#chrome_options.add_experimental_option("useAutomationExtension", False)
	#chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
	#chrome_options.add_argument("user-data-dir=C:/Users/marco/Desktop/FoxyByte/Crawler/Profile") #edit 
	
	#driver = webdriver.Chrome("C:/Users/marco/Desktop/FoxyByte/Crawler/chromedriver.exe", options=chrome_options) #edit
	driver.get(locationURL)

	time.sleep(10)
	# wait for the page to be fully loaded
	# then scroll down, let it load more posts, scroll down again, until first ever post
	# then continue...

	posts = driver.find_elements_by_css_selector(".FFVAD")
	src_data_array=[]
	for data in posts:
		src_data_array.append(data.get_attribute('src'))
	
	post_src_array=[]
	for src in src_data_array:
		post_src_array.append(src)
	
	return post_src_array
		

















def crawl(url):
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_experimental_option("useAutomationExtension", False)
	chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
	chrome_options.add_argument("user-data-dir=C:/Users/marco/Desktop/FoxyByte/Crawler/Profile"); #edit 

	driver = webdriver.Chrome("C:/Users/marco/Desktop/FoxyByte/Crawler/chromedriver.exe", options=chrome_options) #edit
	driver.get(url)
	time.sleep(5)

	print("Reached")
	users_list = []
	users = driver.find_elements_by_class_name('_7UhW9')
	for u in users:
		users_list.append(u.text)

	texts_list = []
	texts = driver.find_elements_by_css_selector('#react-root > section > main > div > div > article > div > div.qF0y9 > div.cv3IO > div.eo2As > div.EtaWk > ul > ul > div > li > div > div > div.C4VMK > div.MOdxS > span')
	comments_count = 0
	for txt in texts:
		texts_list.append(txt.text)

	max_len = 0
	if len(users_list) > len(texts_list):
		max_len = len(users_list)
	else:
		max_len = len(texts_list)

	for i in range(max_len):
		if i < len(users_list):
			print("User: ",users_list[i])
		if i < len(texts_list):
			print("Text: ",texts_list[i])
	#next_url = driver.find_elements_by_css_selector(".v1Nh3 kIKUG _bz0w [href]")
	#next_url = driver.find_elements_by_tag_name("a")
	#for u in next_url:
		#print(u.get_attribute('href'))


def login():

	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_experimental_option("useAutomationExtension", False)
	chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
	chrome_options.add_argument("user-data-dir=C:/Users/marco/Desktop/FoxyByte/Crawler/Profile"); #edit 
	
	driver = webdriver.Chrome("C:/Users/marco/Desktop/FoxyByte/Crawler/chromedriver.exe", options=chrome_options) #edit
	getdriver = ("https://www.instagram.com/accounts/login/")
	
	username = "foxybyte.swe"
	password = "Swe_2022"

	driver.get(getdriver)

	time.sleep(300)

# Instead of crawling through the login and cookies popup every time,
# it is easier to create a custom profile for the crawler, so that cookies are 
# already saved and ready to go, making the crawling less of a headache

# Deprecated code:

#	time.sleep(5)
#	allowButton = driver.find_element_by_css_selector("button[tabindex='0']").click()
#	time.sleep(5)
#	driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
#	driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
#	driver.find_element_by_xpath("//button[contains(.,'Accedi')]").click()
#	time.sleep(50)
#	driver.find_element_by_css_selector("button[tabindex='0']").click()
#	time.sleep(5)
#	driver.find_element_by_css_selector("button[tabindex='0']").click()
#	time.sleep(5)

#url = "https://www.instagram.com/p/CaUwlR_hS-q"
#crawl(url)

#################################################################

def main():	
	driver = buildWebDriver()

	url = getLocationPageBySearchBar("Al Saiso", driver)
	posts_array = crawlLocation(url, driver)
	print("returned the following post image links: \n")
	print(posts_array)


################################################################

if __name__ == "__main__":
    main()
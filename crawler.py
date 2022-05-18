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


def crawlCity(nation, nationISOCode, city):
	baseLocationURL= "www.instagram.com/explore/locations"
	cityLocationURL=  baseLocationURL + "/" + nationISOCode + "/" + nation
	
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_experimental_option("useAutomationExtension", False)
	chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

	driver = webdriver.Chrome("path/to/webdriver", options=chrome_options)
	driver.get(cityLocationURL)
	texts = driver.find_elements_by_css_selector('#react-root > section > main > div class  > div')

# M1: main page -> search restaurant -> get location href
# M2: locations -> search for city name -> get location href (not all cities are present)
#
#
#


def crawlSpecificLocation(locationURL):
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_experimental_option("useAutomationExtension", False)
	chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

	driver = webdriver.Chrome("C:/Users/marco/OneDrive/Marco/UniPD/Triennale/Ingegneria del Software/Progetto/FoxyByte/chromedriver.exe", options=chrome_options)
	driver.get(locationURL)

	posts = driver.find_elements_by_css_selector('#react-root > section > main > article  > div > div > div > div > div > a > div > div > img')
	




def crawl(url):
	driver = webdriver.Chrome("C:/Users/marco/OneDrive/Marco/UniPD/Triennale/Ingegneria del Software/Progetto/FoxyByte/chromedriver.exe")
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
	login()



################################################################

if __name__ == "__main__":
    main()
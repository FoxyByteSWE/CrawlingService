import requests
import os, json, sys
import sys, time, os, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if os.name == 'posix':
	chromedriverDirectory = (str(sys.path[0]))+"/../chromedriver"
else:
	chromedriverDirectory = (str(sys.path[0]))+"/../chromedriver.exe"

def buildWebDriver():
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_experimental_option("useAutomationExtension", False)
	chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
	driver = webdriver.Chrome(chromedriverDirectory, options=chrome_options)
	return driver


def find():
	#does instagrapi have some name based search method? shall we use Selenium instead?
	# 1. scrape restaurant location
	# 2. compare username of profiles to restaurant location name: need to find a way to find SIMILAR names, not exact matches, which would be uncommon.
	#	this can be done with calculating a likelihood of the name being a possible match. https://stackoverflow.com/questions/10473745/compare-strings-javascript-return-of-likely
	# 3. if found, get profile picture of said account. If not, well... discard the restaurant all together, they have to be on instagram to be on our site.


def main():




if __name__ == "__main__":
    main()

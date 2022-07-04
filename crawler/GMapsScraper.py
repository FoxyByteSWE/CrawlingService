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



def getMainLocationImageFromGMaps(locationName, driver):
    driver.get("https://www.google.com/maps/search/?api=1&query="+locationName)
    time.sleep(5)
    cover_img = driver.find_element(By.XPATH, "//img[@decoding='async']")
    src = cover_img.get_property("src")
    return src

def main():
    driver=buildWebDriver()
    source= getMainLocationImageFromGMaps("Al Saiso",driver)
    print(source)



if __name__ == "__main__":
    main()

import json
import sys, os
import datetime
from geopy.geocoders import Nominatim
from math import exp
from pprint import pprint
import datetime

from Media import Media

sys.path.insert(1, (str(sys.path[0]))+"/../../RankingService/")

from ComprehendClient import ComprehendClient
from RekognitionClient import RekognitionClient



# GMaoScraoer
import requests
import os, json, sys
import sys, time, os, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
if os.name == 'posix':
	#chromedriverDirectory = (str(sys.path[0]))+"/../chromedriver"
	chromedriverDirectory = (str(sys.path[0]))+"/../IGCrawlerService/chromedriver"
else:
	#chromedriverDirectory = (str(sys.path[0]))+"/../chromedriver.exe"
	chromedriverDirectory = (str(sys.path[0]))+"/../IGCrawlerService/chromedriver.exe"



class Restaurant:

	def __init__(self, pk = 0, medias = [], name = "", category = "", address = "", website = "", phone = "", main_image_url = "", coordinates = "", ranking = -1):
		self.pk = pk
		self.medias = medias
		self.name = name
		self.category = category
		self.address = address
		self.website = website
		self.phone = phone
		self.main_image_url = main_image_url
		self.coordinates = coordinates
		self.ranking = ranking

	def assignValues(self):
		for m in self.medias:
			if self.name == "" and m.TakenAtLocation["name"] != "":
				self.name = m.TakenAtLocation["name"]
			if self.category == "" and m.TakenAtLocation["category"] != "":
				self.category = m.TakenAtLocation["category"]
			#if self.address == "" and m.TakenAtLocation["address"] != "":
				#self.address = m.TakenAtLocation["address"]
			if self.website == "" and m.TakenAtLocation["website"] != "":
				self.website = m.TakenAtLocation["website"]
			if self.phone == "" and m.TakenAtLocation["phone"] != "":
				self.phone = m.TakenAtLocation["phone"]
			if self.coordinates == "" and m.TakenAtLocation["coordinates"] != "":
				self.coordinates = m.TakenAtLocation["coordinates"]
		geolocator = Nominatim(user_agent="geoapiExercises")
		self.address = geolocator.reverse(str(self.coordinates[1]) + "," + str(self.coordinates[0]))
		#self.main_image_url = self.getMainImageUrl()

	def returnFormattedRanking(self):
		return '{0:.1f}'.format(self.ranking)

	def printFormattedRanking(self):
		print('{0:.1f}'.format(self.ranking))

	def isOld(self, m):
		now = datetime.datetime.now()
		post_taken_at = datetime.datetime(m.TakenAtTime[0], m.TakenAtTime[1], m.TakenAtTime[2], m.TakenAtTime[3], m.TakenAtTime[4], m.TakenAtTime[5])
		age = (now - post_taken_at).days
		if age > 1800:
			return True
		else:
			return False
	
	def removeOldMedias(self):
		self.medias = [m for m in self.medias if not self.isOld(m)]



	def buildWebDriver(self):
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_experimental_option("useAutomationExtension", False)
		chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
		driver = webdriver.Chrome(chromedriverDirectory, options=chrome_options)
		return driver

	def getMainLocationImageFromGMaps(self, locationName, driver):
		driver.get("https://www.google.com/maps/search/?api=1&query="+locationName)
		time.sleep(20)
		try:
			cover_img = driver.find_element(By.XPATH, "//img[@decoding='async']")
		except Exception as e:
			print(e)
			return ""
		src = cover_img.get_property("src")
		return src

	def getMainImageUrl(self):
		driver = self.buildWebDriver()
		source = self.getMainLocationImageFromGMaps(self.name + " " + str(self.address), driver)
		return source





def rank(restaurants):

	comprehend = ComprehendClient()
	rekognition = RekognitionClient()

	for r in restaurants:
		pos = neg = neu = mix = 0
		weight_list = []
		#print("Comments for restaurant " + r.pk)

		for m in r.medias:
			now = datetime.datetime.now()
			post_taken_at = datetime.datetime(m.TakenAtTime[0], m.TakenAtTime[1], m.TakenAtTime[2], m.TakenAtTime[3], m.TakenAtTime[4], m.TakenAtTime[5])
			age = (now - post_taken_at).days
			#print(age)

			if age <= 90:
				weight = 1
			elif age <= 360:
				weight = 0.9
			elif age <= 720:
				weight = 0.7
			elif age <= 1080:
				weight = 0.5
			elif age <= 1800:
				weight = 0.2
			else:
				weight = 0

			if m.CaptionText != "":
				#print(m.CaptionText)
				score = comprehend.analyzeText(m.CaptionText)
				pos += score["Positive"] * weight
				neg += score["Negative"] * weight
				#neu += score["Neutral"] * weight
				#mix += score["Mixed"] * weight
				weight_list.append(weight)

		if sum(weight_list) == 0:
			pos = neg = 0
		else:
			pos /= sum(weight_list)
			neg /= sum(weight_list)
			#neu /= sum(weight_list)
			#mix /= sum(weight_list)

		ranking = pos-neg
		ranking = linearRanking(ranking)
		#ranking = sigmoidRanking(ranking)
		ranking = round(ranking, 1)

		r.ranking = ranking

def linearRanking(x):
	x = 5*x + 5
	return x

def sigmoidRanking(x):
	x = 1 / (1 + exp(-5*x))
	x = 10*x
	return x

		
def json2Restaurants(path):

	with open(path, 'r') as inputfile:
		data = json.load(inputfile)

	restaurant_list = []

	for restaurant in data:
		media_list = []

		for media in data[restaurant]:
			m = Media(media["PostPartialURL"], media["MediaType"], media["TakenAtTime"], media["TakenAtLocation"], media["LikeCount"], media["CaptionText"], media["MediaURL"])
			media_list.append(m)

		restaurant_list.append(Restaurant(restaurant, media_list))

	return restaurant_list

def Restaurants2json(restaurants, file):
	out = '{'
	for r in restaurants:
		out += '"' + r.pk + '": ['
		for m in r.medias:
			out += json.dumps(m.__dict__)
			out += ', '
		out = out[:-2]
		out += '], '

	out = out[:-2]
	out += '}'
	f = open(file, "w")
	f.write(out)
	f.close()


def removeOldMedias(restaurants):
	for r in restaurants:
		r.removeOldMedias()

def main():
	restaurants = json2Restaurants((str(sys.path[0]))+"/data/locationsData.json")
	for r in restaurants:
		r.assignValues()

	for r in restaurants:
		pprint(vars(r))
		for m in r.medias:
			pprint(vars(m))

	Restaurants2json(restaurants, (str(sys.path[0]))+"/data/test_Restaurants2json.json")

	removeOldMedias(restaurants)

	for r in restaurants:
		pprint(vars(r))
		for m in r.medias:
			pprint(vars(m))

	rank(restaurants)
	for r in restaurants:
		print(r.pk)
		print(r.name)
		r.printFormattedRanking()
		print('\n')

if __name__ == "__main__":
	main()

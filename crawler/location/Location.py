import json
import sys, os
import datetime
from math import exp
from pprint import pprint

from crawler.location.Location import Location



class Location:

	def __init__(self, pk = 0, name = "", category = "", address = "", website = "", phone = "", main_image_url = "", coordinates = {}, latest_post_partial_url_checked = ""):
		self.pk = pk
		self.name = name
		self.category = category
		self.address = address
		self.website = website
		self.phone = phone
		self.main_image_url = main_image_url
		self.coordinates = coordinates
		self.latest_post_partial_url_checked = latest_post_partial_url_checked


	def convertToDict(self):
		pass

	def getPk(self):
		return self.pk
	
	def getName(self):
		return self.name

	def getCategory(self):
		return self.category

	def getAddress(self):
		return self.address

	def getCoordinates(self):
		return self.coordinates

	def getWebsite(self):
		return self.website

	def getPhone(self):
		return self.phone
	
	def getMainImageUrl(self):
		return self.main_image_url

	def getLatestPostPartialURLChecked(self):
		return self.latest_post_partial_url_checked

	def setLatestPostPartialUrlChecked(self, newCode):
		self.latest_post_partial_url_checked = newCode

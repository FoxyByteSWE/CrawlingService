import json
import sys, os
import datetime
from pprint import pprint


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
		item = {}
		item['pk'] = self.pk
		item['name'] = self.name
		item['category'] = self.category
		item['address'] = self.address
		item['website'] = self.website
		item['phone'] = self.phone
		item['main_image_url'] = self.main_image_url
		item['coordinates_lng'] = self.coordinates['lng']
		item['coordinates_lat'] = self.coordinates['lat']
		item['latest_post_partial_url_checked'] = self.latest_post_partial_url_checked
		return item

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

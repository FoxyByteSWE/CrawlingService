import os, json, sys, time
from instagrapi import Client
import instagrapi
from typing import Dict
import pprint

import LocationProfileFinder
from InstagrapiUtils import InstagrapiUtils
from JSONUtils import JSONUtils
from Config import CrawlingServiceConfig
from media.FoxyByteMedia import FoxyByteMedia
from media.FoxyByteMediaFactory import FoxyByteMediaFactory
from location.Location import Location
from DBConnection import DBConnection

#proxy = 'http://96.9.71.18:33427'

#os.environ['http_proxy'] = proxy 
#os.environ['HTTP_PROXY'] = proxy
#os.environ['https_proxy'] = proxy
#os.environ['HTTPS_PROXY'] = proxy


class Crawler:

	def __init__(self) -> None:
		self.instagrapiUtils = InstagrapiUtils()
		self.db = DBConnection()



	def saveCrawledDataFromLocation(self, mediasfromloc: dict, locationPK: dict) -> None:
		for media in mediasfromloc:
			self.db.insertMedia(media)

#	def formatMediaToDictionaryItem(self, media: dict) -> dict: #need to serialize casting to primitive data types
#		formattedDictionaryMedia = {}
#		formattedDictionaryMedia["PostPartialURL"] = self.instagrapiUtils.getPostPartialURL(media)
#		formattedDictionaryMedia["MediaType"] = self.instagrapiUtils.getMediaType(media)
#		formattedDictionaryMedia["TakenAtTime"] = self.parseTakenAtTime(self.instagrapiUtils.getMediaTime(media))
#		formattedDictionaryMedia["TakenAtLocation"] = self.parseTakenAtLocation(media) #extra step necessary.
#		formattedDictionaryMedia["LikeCount"] = self.instagrapiUtils.getMediaLikeCount(media)
#		formattedDictionaryMedia["CaptionText"] = self.instagrapiUtils.getCaptionText(media)
#		formattedDictionaryMedia["MediaURL"] = self.parseMediaUrl(self.instagrapiUtils.getMediaURL(media))
#		#pprint.pprint(formattedDictionaryMedia)
#		return formattedDictionaryMedia





	def isMediaDuplicated(self, media) -> bool:
		query = "SELECT * FROM Media WHERE CODE == " + str(media.code)
		response = self.db.executeQuery(query)
		if response != None:
			return True
		else:
			return False





	#MAIN CRAWLING FUNCTION

	def crawlAllLocations(self, locations, nPostsWanted: int) -> None:
		for location in locations.values():
			mediasDump = self.instagrapiUtils.getMostRecentMediasFromLocation(location.name, nPostsWanted) #returns a list of "Medias"

			mediasFromLocation = []

			for media in mediasDump:

				parsedtakenat = self.instagrapiUtils.parseTakenAtTime(media.taken_at)
				parsedlocation = self.instagrapiUtils.parseTakenAtLocation(media)
				parsedmediaurl = self.instagrapiUtils.parseMediaUrl(self.instagrapiUtils.getMediaURL(media))

				newmedia = FoxyByteMediaFactory.buildFromInstagrapiMediaAndLocation(media, parsedtakenat, parsedlocation, parsedmediaurl)

				if self.isMediaDuplicated(newmedia) == False: # check in database
						print("media appended.")
						mediasFromLocation.append(mediasFromLocation) 

			if mediasFromLocation != []:
				print("saving medias...")
				self.saveCrawledDataFromLocation(mediasFromLocation, location.pk)
			

			






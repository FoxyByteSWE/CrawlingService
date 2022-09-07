import os, json, sys, time
from instagrapi import Client
import instagrapi
from typing import Dict
import pprint

import LocationProfileFinder
from InstagrapiUtils import InstagrapiUtils
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



	def saveMediaFromLocation(self, media: dict, locationPK: dict) -> None:
			self.db.insertMedia(media)


	def isMediaDuplicated(self, media) -> bool:
		query = "SELECT * FROM Media WHERE CODE == " + str(media.code)
		response = self.db.executeQuery(query)
		if response != None:
			return True
		else:
			return False




	def checkIfPostIsNew(self, indexedPURL: str, latestPURL: str) -> bool:
		if latestPURL == indexedPURL:
			return False
		else:
			return True

	def parseNonPrimitiveMediaData(self, media):
		parsedtakenat = self.instagrapiUtils.parseTakenAtTime(media.taken_at)
		parsedlocation = self.instagrapiUtils.parseTakenAtLocation(media)
		parsedmediaurl = self.instagrapiUtils.parseMediaUrl(self.instagrapiUtils.getMediaURL(media))
		return [parsedtakenat, parsedlocation, parsedmediaurl]

	#MAIN CRAWLING FUNCTION

	def crawlLocation(self, location, nPostsWanted: int) -> None:
		mediasDump = self.instagrapiUtils.getMostRecentMediasFromLocation(location.name, nPostsWanted) #returns a list of "Medias"

		mediasFromLocation = []
		lastpostcodechecked = location.getLastPostCheckedCode()


		for media in mediasDump:

			if self.checkIfPostIsNew(media.code, lastpostcodechecked) == False:  # check if reached a post already checked before
				return
			
			parsedMediaData = self.parseNonPrimitiveMediaData(media)
			newmedia = FoxyByteMediaFactory.buildFromInstagrapiMediaAndLocation(media, parsedMediaData[0], parsedMediaData[1], parsedMediaData[2])

			if self.isMediaDuplicated(newmedia) == False:
					self.saveMediaFromLocation(mediasFromLocation, location.pk)

				
			

			






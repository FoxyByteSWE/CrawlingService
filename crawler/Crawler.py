import os, json, sys, time
from instagrapi import Client
import instagrapi
from typing import Dict
import pprint

import RestaurantProfileFinder
from InstagrapiUtils import InstagrapiUtils
from JSONUtils import JSONUtils
from Config import CrawlingServiceConfig
from media.FoxyByteMedia import FoxyByteMedia
from media.FoxyByteMediaFactory import FoxyByteMediaFactory

#proxy = 'http://96.9.71.18:33427'

#os.environ['http_proxy'] = proxy 
#os.environ['HTTP_PROXY'] = proxy
#os.environ['https_proxy'] = proxy
#os.environ['HTTPS_PROXY'] = proxy


class Crawler:

	jsonUtils = JSONUtils()
	instagrapiUtils = InstagrapiUtils()


	def readFromJSON(self, processing_strategy: JSONUtils.ReadJSONStrategy):
		return processing_strategy.readFromJSON(self)

	def writeToJSON(self, data, processing_strategy: JSONUtils.WriteJSONStrategy):
		return processing_strategy.writeToJSON(self, data)


	def saveCrawledDataFromLocation(self, mediasfromloc: dict, locationPK: dict) -> None:
		locationsFromJSON = self.readFromJSON(JSONUtils.CrawledDataReadJSONStrategy)
		try:
			locobj=locationsFromJSON[locationPK] #lista di dizionari
			locobj.append(mediasfromloc)
			locationsFromJSON[locationPK]=locobj
		except KeyError:
			locationsFromJSON[locationPK] = mediasfromloc
		self.writeToJSON(locationsFromJSON,JSONUtils.CrawledDataWriteJSONStrategy)


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





	def isMediaDuplicated(self, media, locationPk: int) -> bool:
		print("e")
		try:
			fromjson = self.readFromJSON(JSONUtils.CrawledDataReadJSONStrategy)
		except json.JSONDecodeError:
			print("f")
			return False
		locationPk= str(locationPk)
		if locationPk in fromjson.keys():
			singlelocationdata=fromjson[locationPk]  #lista di dizionari
			for item in singlelocationdata:	
				if media["PostPartialURL"] == item["PostPartialURL"]:
					#print("dup")
					return True
				else:
					print(str(media["PostPartialURL"]) + " is not a dup of " + str(item["PostPartialURL"]))
			return False
		return False





	#MAIN CRAWLING FUNCTION

	def crawlAllLocations(self, locationsDict: dict, nPostsWanted: int) -> None:
		for loc in locationsDict.values():
			mediasDump = self.instagrapiUtils.getMostRecentMediasFromLocation(loc["name"]) #returns a list of "Medias"

			formattedMediasFromLocation = []
			locationPk = loc["pk"]
			foundRestaurantProfile = False


			for media in mediasDump:
				if RestaurantProfileFinder.checkForRestaurantUsername(media, loc["name"]) == True:
					foundRestaurantProfile = True

			if foundRestaurantProfile == True:
				for media in mediasDump[0:nPostsWanted-1]:
					#print("a")
					#uname = (media.user).username
					#print("b")
					##propic = self.parseMediaUrl(client.user_info_by_username(uname).profile_pic_url)
					##self.parseMediaUrl(self.instagrapiUtils.getUserInfoByUsername(uname).profile_pic_url)
					#print("c")
					##print(propic)

					parsedtakenat = self.instagrapiUtils.parseTakenAtTime(media.taken_at)
					parsedlocation = self.instagrapiUtils.parseTakenAtLocation(media)
					parsedmediaurl = self.instagrapiUtils.parseMediaUrl(self.instagrapiUtils.getMediaURL(media))

					newmedia = FoxyByteMediaFactory.buildFromInstagrapiMediaAndLocation(media, parsedtakenat, parsedlocation, parsedmediaurl)

					if self.isMediaDuplicated(newmedia,locationPk) == False: # check in database
							print("media appended.")
							#formattedMediasFromLocation.append(formattedmedia) 
				if formattedMediasFromLocation != []:
					print("saving medias...")
					self.saveCrawledDataFromLocation(formattedMediasFromLocation, locationPk)  # Questo dovrebbe essere solo alla fine del crawling di una location (primo ciclo for). Qui dovrebbe solo accumulare in un dizionario.
			else:
				print("No Profile Found, discarding restaurant.")
			

			



	def beginCrawling(self, nPostsWanted: int) -> None:
		locationsDict = self.readFromJSON(JSONUtils.TrackedLocationsReadJSONStrategy)
		self.crawlAllLocations(locationsDict, 2)


import os, json, sys, time
from instagrapi import Client
import instagrapi
from typing import Dict
import pprint

import RestaurantProfileFinder
from InstagrapiUtils import InstagrapiUtils
from JSONUtils import JSONUtils
from Config import CrawlingServiceConfig

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


	def saveCrawledDataFromLocation(self, mediasfromloc, locationPK):
		locationsFromJSON = self.readFromJSON(JSONUtils.CrawledDataReadJSONStrategy)
		try:
			locobj=locationsFromJSON[locationPK] #lista di dizionari
			locobj.append(mediasfromloc)
			locationsFromJSON[locationPK]=locobj
		except KeyError:
			locationsFromJSON[locationPK] = mediasfromloc
		self.writeToJSON(locationsFromJSON,JSONUtils.CrawledDataWriteJSONStrategy)


	def formatMediaToDictionaryItem(self, media): #need to serialize casting to primitive data types
		formattedDictionaryMedia = {}
		formattedDictionaryMedia["PostPartialURL"] = self.instagrapiUtils.getPostPartialURL(media)
		formattedDictionaryMedia["MediaType"] = self.instagrapiUtils.getMediaType(media)
		formattedDictionaryMedia["TakenAtTime"] = self.parseTakenAtTime(self.instagrapiUtils.getMediaTime(media))
		formattedDictionaryMedia["TakenAtLocation"] = self.parseTakenAtLocation(media) #extra step necessary.
		formattedDictionaryMedia["LikeCount"] = self.instagrapiUtils.getMediaLikeCount(media)
		formattedDictionaryMedia["CaptionText"] = self.instagrapiUtils.getCaptionText(media)
		formattedDictionaryMedia["MediaURL"] = self.parseMediaUrl(self.instagrapiUtils.getMediaURL(media))
		#pprint.pprint(formattedDictionaryMedia)
		return formattedDictionaryMedia





	def buildComprehendLocationDictionary(self, locationpk):
		locationsData = self.readFromJSON(JSONUtils.CrawledDataReadJSONStrategy)

		comprehendDict = {}
		location = locationsData[locationpk]

		for post in location:
			comprehendDict[post["PostPartialURL"]] = post["CaptionText"]
		pprint.pprint(comprehendDict)
		return comprehendDict


	def parseTakenAtTime(self, input):
		time = []
		time.append(input.year)
		time.append(input.month)
		time.append(input.day)
		time.append(input.hour)
		time.append(input.minute)
		time.append(input.second)
		return time

	def parseTakenAtLocation(self, media):
		input = self.instagrapiUtils.getDetailedMediaLocationInfo(media).dict()
		coordinates = self.instagrapiUtils.getMediaLocationCoordinates(media)
		dict = {}
		dict["pk"] = input["pk"]
		dict["name"] = input["name"]
		dict["address"] = input["address"]
		dict["coordinates"] = [coordinates["lng"], coordinates["lat"]]
		dict["category"] = input["category"]
		dict["phone"] = input["phone"]
		dict["website"] = input["website"]
		return dict;

	def parseMediaUrl(self, input):
		url = str(input)
		start = url.find("'") + 1
		url = url[start:]
		end = url.find("'")
		url = url[:end]
		return url;



	def isMediaDuplicated(self, media, locationPk):
		fromjson = self.readFromJSON(JSONUtils.CrawledDataReadJSONStrategy)
		if fromjson == {}:  # meaning it is empty
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


	#MAIN CRAWLING FUNCTIONS

	def crawlAllLocations(self, locationsDict: dict, nPostsWanted: int):
		for loc in locationsDict.values():
			mediasDump = self.instagrapiUtils.getMostRecentMediasFromLocation(loc["name"]) #returns a list of "Medias"
			mediasDump = [media.dict() for media in mediasDump]

			formattedMediasFromLocation = []
			locationPk = loc["pk"]
			foundRestaurantProfile = False
			for media in mediasDump:
				if RestaurantProfileFinder.checkForRestaurantUsername(media, loc["name"]) == True:
					foundRestaurantProfile = True
			if foundRestaurantProfile == True:
				for media in mediasDump[0:nPostsWanted-1]:
					uname = media.user.username
					#propic = self.parseMediaUrl(client.user_info_by_username(uname).profile_pic_url)
					self.parseMediaUrl(self.instagrapiUtils.getUserInfoByUsername(uname).profile_pic_url)
					#print(propic)
					formattedmedia = self.formatMediaToDictionaryItem(media)
					if self.isMediaDuplicated(formattedmedia,locationPk) == False:
							print("media appended.")
							formattedMediasFromLocation.append(formattedmedia) 
				if formattedMediasFromLocation != []:
					print("saving medias...")
					self.saveCrawledDataFromLocation(formattedMediasFromLocation, locationPk)  # Questo dovrebbe essere solo alla fine del crawling di una location (primo ciclo for). Qui dovrebbe solo accumulare in un dizionario.
			else:
				print("No Profile Found, discarding restaurant.")
			

			



	def beginCrawling(self, nPostsWanted):
		locationsDict = self.readFromJSON(JSONUtils.TrackedLocationsReadJSONStrategy)
		self.crawlAllLocations(locationsDict, nPostsWanted)


	###########	





#def main():
#	
#	self.beginCrawling()
#
#################################################################
#
#if __name__ == "__main__":
#	main()




########################################

# UNIT TESTS



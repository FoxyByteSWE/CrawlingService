import os, json, sys, time
from instagrapi import Client
import instagrapi
from typing import Dict
import pprint

import RestaurantProfileFinder
from InstagrapiUtils import InstagrapiUtils

#proxy = 'http://96.9.71.18:33427'

#os.environ['http_proxy'] = proxy 
#os.environ['HTTP_PROXY'] = proxy
#os.environ['https_proxy'] = proxy
#os.environ['HTTPS_PROXY'] = proxy


class Crawler:
	
	def getAllCrawlableLocationsFromJSON():
		filepath = (str(sys.path[0]))+"/data/locations.json"
		with open(filepath) as locations:
			try:
				data = json.load(locations)
				return data
			except Exception as e:
				print(e)
				return False

	def readLocationsDataFromJSON():
		filepath = (str(sys.path[0]))+"/data/locationsData.json"
		with open(filepath) as locationsData:
			try:
				data = json.load(locationsData)
				return data
			except Exception as e:
				print(e)
				return None


	def writeCrawledDataToJson(locationsData): 
		jsondump= json.dumps(locationsData)
		with open((str(sys.path[0]))+"/data/locationsData.json", "w") as outfile:
			outfile.write(jsondump)


	def getCrawledDataFromJSON():
		filepath = (str(sys.path[0]))+"/data/locationsData.json"
		with open(filepath) as locationsFile:
			try:
				data = json.load(locationsFile)
				return data
			except Exception as e:
				print(e)
				return {}
		

	def saveCrawledDataFromLocationToJSON(mediasfromloc, locationPK):
		locationsFromJSON = Crawler.getCrawledDataFromJSON()
		try:
			locobj=locationsFromJSON[locationPK] #lista di dizionari
			locobj.append(mediasfromloc)
			locationsFromJSON[locationPK]=locobj
		except KeyError:
			locationsFromJSON[locationPK] = mediasfromloc
		Crawler.writeCrawledDataToJson(locationsFromJSON)




	def formatMediaToDictionaryItem(media,client): #need to serialize casting to primitive data types
		formattedDictionaryMedia = {}
		formattedDictionaryMedia["PostPartialURL"] = InstagrapiUtils.getPostPartialURL(media)
		formattedDictionaryMedia["MediaType"] = InstagrapiUtils.getMediaType(media)
		formattedDictionaryMedia["TakenAtTime"] = Crawler.parseTakenAtTime(InstagrapiUtils.getMediaTime(media))
		formattedDictionaryMedia["TakenAtLocation"] = Crawler.parseTakenAtLocation(media,client) #extra step necessary.
		formattedDictionaryMedia["LikeCount"] = InstagrapiUtils.getMediaLikeCount(media)
		formattedDictionaryMedia["CaptionText"] = InstagrapiUtils.getCaptionText(media)
		formattedDictionaryMedia["MediaURL"] = Crawler.parseMediaUrl(InstagrapiUtils.getMediaURL(media))
		#pprint.pprint(formattedDictionaryMedia)
		return formattedDictionaryMedia





	def buildComprehendLocationDictionary(locationpk):
		locationsData = Crawler.readLocationsDataFromJSON()

		comprehendDict = {}
		location = locationsData[locationpk]

		for post in location:
			comprehendDict[post["PostPartialURL"]] = post["CaptionText"]
		pprint.pprint(comprehendDict)
		return comprehendDict


	def parseTakenAtTime(input):
		time = []
		time.append(input.year)
		time.append(input.month)
		time.append(input.day)
		time.append(input.hour)
		time.append(input.minute)
		time.append(input.second)
		return time

	def parseTakenAtLocation(media, client):
		input = InstagrapiUtils.getDetailedMediaLocationInfo(media, client).dict()
		coordinates = InstagrapiUtils.getMediaLocationCoordinates(media)
		dict = {}
		dict["pk"] = input["pk"]
		dict["name"] = input["name"]
		dict["address"] = input["address"]
		dict["coordinates"] = [coordinates["lng"], coordinates["lat"]]
		dict["category"] = input["category"]
		dict["phone"] = input["phone"]
		dict["website"] = input["website"]
		return dict;

	def parseMediaUrl(input):
		url = str(input)
		start = url.find("'") + 1
		url = url[start:]
		end = url.find("'")
		url = url[:end]
		return url;



	def isMediaDuplicated(media, locationPk):
		fromjson = Crawler.getCrawledDataFromJSON()
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

	def crawlAllLocations(locationsDict, client, nPostsWanted):
		for loc in locationsDict.values():
			mediasDump = InstagrapiUtils.getTopMediasFromLocation(loc["name"], client) #returns a list of "Medias"
			#mediasDump = InstagrapiUtils.getMostRecentMediasFromLocation(loc["name"], client) #returns a list of "Medias"
			formattedMediasFromLocation = []
			locationPk = loc["pk"]
			for media in mediasDump[0:nPostsWanted-1]:
				if RestaurantProfileFinder.checkForRestaurantUsername(media, loc["name"]) == True:
					
					uname = media.user.username
					propic = Crawler.parseMediaUrl(client.user_info_by_username(uname).profile_pic_url)
					#print(propic)
					formattedmedia = Crawler.formatMediaToDictionaryItem(media,client)
					if Crawler.isMediaDuplicated(formattedmedia,locationPk) == False:
							formattedMediasFromLocation.append(formattedmedia) 
					if formattedMediasFromLocation != []:
						Crawler.saveCrawledDataFromLocationToJSON(formattedMediasFromLocation, locationPk)
				else:
					print("No Profile Found, discarding restaurant.")
					

			



	def beginCrawling():
		client = InstagrapiUtils.createLoggedInClient()
		locationsDict = Crawler.getAllCrawlableLocationsFromJSON()
		nPostsWanted = 50 # only get N top posts from each location
		locationsData = Crawler.crawlAllLocations(locationsDict, client, nPostsWanted)


	###########	





def main():
	Crawler.beginCrawling()

################################################################

if __name__ == "__main__":
	main()




########################################

# UNIT TESTS



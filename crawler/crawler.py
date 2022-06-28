import os, json, sys
from instagrapi import Client
import instagrapi
from typing import Dict
import pprint

#proxy = 'http://96.9.71.18:33427'

#os.environ['http_proxy'] = proxy 
#os.environ['HTTP_PROXY'] = proxy
#os.environ['https_proxy'] = proxy
#os.environ['HTTPS_PROXY'] = proxy

def createLoggedInClient():
	client = Client()
	client.login("foxybyte.swe", "Swe_2022")
	#client.dump_settings((str(sys.path[0]))+"/data/settingsdump.json")
	#client.load_settings((str(sys.path[0]))+"/data/settingsdump.json")
	return client


#############################################

# LOCATION GETTERS


def getAllCrawlableLocationsFromJSON():
	filepath = (str(sys.path[0]))+"/data/locations.json"
	with open(filepath) as locations:
		try:
			data = json.load(locations)
			return data
		except Exception as e:
			print(e)
			return False

def getLocationPkCodeFromName(locationName, client):
	locList = (client.fbsearch_places(locationName)[0]).dict()
	pkCode = locList.get("pk")
	return pkCode


def getTopMediasFromLocation(locationName, client):
	pkCode = getLocationPkCodeFromName(locationName, client)
	mediaListFromLocation = client.location_medias_top(pkCode)
	return mediaListFromLocation

def writeCrawledDataToJson(locationsData): 
	jsondump= json.dumps(locationsData)
	with open((str(sys.path[0]))+"/data/locationsData.json", "a") as outfile:
		outfile.write(jsondump)




###################################################

# GETTERS FOR FORMATTEDMEDIADICTIONARY

def getMediaType(media):
	return media.media_type

def getCaptionText(media):
	return media.caption_text

def getMediaTime(media):
	return media.taken_at

def getMediaLocationCoordinates(media):
	coordinates = {'lng': (media.location).lng , 
				   'lat': (media.location).lat }
	return coordinates


def getMediaLocationPK(media):
		return media.pk

def getMediaLikeCount(media):
	return media.like_count

def getMediaURL(media):
	if getMediaType(media)==1:
		return media.thumbnail_url
	if getMediaType(media)==2:
		return media.video_url
	if getMediaType(media)==8: #album
		album = media.resources
		list=[]
		for item in album:
			if getMediaType(item) == 1:
				list.append(item.thumbnail_url)
			elif getMediaType(item) == 2:
				list.append(item.video_url)
		return list

def getPostPartialURL(media):
	return media.code

def formatMediaToDictionaryItem(media,client): #need to serialize casting to primitive data types
	formattedDictionaryMedia = {}
	formattedDictionaryMedia["PostPartialURL"] = getPostPartialURL(media)
	formattedDictionaryMedia["MediaType"] = getMediaType(media)
	formattedDictionaryMedia["TakenAtTime"] = parseTakenAtTime(getMediaTime(media))
	formattedDictionaryMedia["TakenAtLocation"] = parseTakenAtLocation(media,client) #extra step necessary.
	formattedDictionaryMedia["LikeCount"] = getMediaLikeCount(media)
	formattedDictionaryMedia["CaptionText"] = getCaptionText(media)
	formattedDictionaryMedia["MediaURL"] = parseMediaUrl(getMediaURL(media))
	#pprint.pprint(formattedDictionaryMedia)
	return formattedDictionaryMedia


#######################################

# OTHER

def readLocationsDataFromJSON():
	filepath = (str(sys.path[0]))+"/data/locationsData.json"
	with open(filepath) as locationsData:
		try:
			data = json.load(locationsData)
			return data
		except Exception as e:
			print(e)
			return None

def buildComprehendLocationDictionary(locationpk):
	locationsData = readLocationsDataFromJSON()

	comprehendDict = {}
	location = locationsData[locationpk]

	for post in location:
		comprehendDict[post["PostPartialURL"]] = post["CaptionText"]
	pprint.pprint(comprehendDict)
	return comprehendDict

	
def getDetailedMediaLocationInfo(media, client):  # this works and retrieves all category and other data
    mediainfo = client.media_info_v1(media.pk)
    if mediainfo.location != None:
        return client.location_info((mediainfo.location).pk)
    else:
        return None


################################################

# PARSING FUNCTIONS

def parseTakenAtTime(input):
	time = []
	time.append(input.year)
	time.append(input.month)
	time.append(input.day)
	time.append(input.hour)
	time.append(input.minute)
	time.append(input.second)
	return time

def parseTakenAtLocation(media,client):
	input = getDetailedMediaLocationInfo(media, client).dict()
	coordinates = getMediaLocationCoordinates(media)
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




########################################

#MAIN CRAWLING FUNCTIONS

# la politica di ordinamento per le location può essere una coda con priorità in base
# all'ultima volta che una certa location è stata analizzata

def crawlAllLocations(locationsDict, client, nPostsWanted):
	for loc in locationsDict.values():
		mediasDump = getTopMediasFromLocation(loc["name"], client) #returns a list of "Medias"
		formattedMediasFromLocation = []
		locationPk = loc["pk"]
		for media in mediasDump[0:nPostsWanted-1]:
			formattedmedia = formatMediaToDictionaryItem(media,client)
			if isMediaDuplicated(formattedmedia,locationPk) == False:
				formattedMediasFromLocation.append(formattedmedia) 
		saveCrawledDataFromLocationToJSON(formattedMediasFromLocation, locationPk)


def getCrawledDataFromJSON():
	filepath = (str(sys.path[0]))+"/data/locationsData.json"
	with open(filepath) as locationsFile:
		try:
			data = json.load(locationsFile)
			return data
		except Exception as e:
			print(e)
			return None
	

def saveCrawledDataFromLocationToJSON(mediasfromloc, locationPK):
	locationsFromJSON = getCrawledDataFromJSON()
	locationsFromJSON[locationPK].append(mediasfromloc)
	writeCrawledDataToJson(locationsFromJSON)


def isMediaDuplicated(media, locationPk):
	fromjson = getCrawledDataFromJSON()
	if locationPk in fromjson.keys():
		if media["PostPartialURL"] == fromjson[locationPk]["PostPartialURL"]:
			return True
		else:
			return False
	return False

def beginCrawling():
	client = createLoggedInClient()
	locationsDict = getAllCrawlableLocationsFromJSON()
	nPostsWanted = 2 # only get N top posts from each location
	locationsData = crawlAllLocations(locationsDict, client, nPostsWanted)
	writeCrawledDataToJson(locationsData)

###########	





def main():
	beginCrawling()

################################################################

if __name__ == "__main__":
	main()
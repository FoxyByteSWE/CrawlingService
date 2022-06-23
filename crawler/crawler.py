import os, json, sys
from instagrapi import Client
import instagrapi
from typing import Dict

def createLoggedInClient():
	client = Client()
	client.login("foxybyte.swe", "Swe_2022")
	return client

def getAllCrawlableLocationsFromSomewhere():
	txt_file = open((str(sys.path[0]))+"/data/locations.txt", "r")
	content_list = txt_file.readlines()
	return content_list

def getTopMediasFromLocation(locationName, client):
	pkCode = getLocationPkCodeFromName(locationName, client)
	mediaListFromLocation = client.location_medias_top(pkCode)
	return mediaListFromLocation

def getLocationPkCodeFromName(locationName, client):
	locList = (client.fbsearch_places(locationName)[0]).dict()
	pkCode = locList.get("pk")
	return pkCode

def writeCrawledDataToJson(locationsData): 
	jsondump= json.dumps(locationsData)
	with open((str(sys.path[0]))+"/data/locationsData.json", "a") as outfile:
		outfile.write(jsondump)

def crawlAllLocations(locationNamesList, client):
	locationsData = { }
	for loc in locationNamesList:
		mediasDump = getTopMediasFromLocation(loc, client) #returns a list of "Medias"
		formattedMediasFromLocation = []
		for media in mediasDump:
			formattedMediasFromLocation.append(formatMediaToDictionaryItem(media)) 
		locationsData[loc] = formattedMediasFromLocation
	return locationsData


#########

#Main Function 

def beginCrawling():
	client = createLoggedInClient()
	locationNamesList = getAllCrawlableLocationsFromSomewhere()
	locationsData = crawlAllLocations(locationNamesList, client)
	writeCrawledDataToJson(locationsData)

###########	

def getMediaType(media):
	return media.media_type

def getCaptionText(media):
	return media.caption_text

def getMediaTime(media):
	return media.taken_at

def getMediaLocationName(media):
	return media.location

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


def formatMediaToDictionaryItem(media): #need to serialize casting to primitive data types
	formattedDictionaryMedia = {}
	formattedDictionaryMedia["MediaType"] = getMediaType(media)
	formattedDictionaryMedia["TakenAtTime"] = parseTakenAtTime(getMediaTime(media))
	formattedDictionaryMedia["TakenAtLocation"] = getMediaLocationName(media).dict()
	formattedDictionaryMedia["LikeCount"] = getMediaLikeCount(media)
	formattedDictionaryMedia["CaptionText"]=getCaptionText(media)
	formattedDictionaryMedia["MediaURL"] = getMediaURL(media)
	print(formattedDictionaryMedia)
	return formattedDictionaryMedia


def updateLocationList():
	# fetch list of locations to crawl from Google Places
	pass
	

def parseTakenAtTime(input):
	time = []
	time.append(input.year)
	time.append(input.month)
	time.append(input.day)
	time.append(input.hour)
	time.append(input.minute)
	time.append(input.second)
	return time

def main():
	updateLocationList()
	beginCrawling()

################################################################

if __name__ == "__main__":
    main()


#	{'Lunaelaltro\n': [{'MediaType': 1, 
# 						'TakenAtTime': datetime.datetime(2016, 4, 15, 18, 19, 44, tzinfo=datetime.timezone.utc), 
# 						'TakenAtLocationName': Location(pk=3110887, name='Ristorante Pizzeria Lunaelaltro - Marostica', phone='', website='', category='', hours={}, address=None, city=None, zip=None, lng=11.660707634193, lat=45.736862428411, external_id=77610911328, external_id_source='facebook_places'), ù
# 						'LikeCount': 1, 
# 						'MediaURL': HttpUrl('https://scontent-mxp2-1.cdninstagram.com/v/t51.2885-15/11249882_966261376755731_963030927_n.jpg?se=8&stp=dst-jpg_e35&_nc_ht=scontent-mxp2-1.cdninstagram.com&_nc_cat=111&_nc_ohc=QeSTLR-83PoAX_ePcKi&edm=AKmAybEBAAAA&ccb=7-5&ig_cache_key=MTIyOTEzNTQ0NTAwMDU1ODY0Mg%3D%3D.2-ccb7-5&oh=00_AT90D8dLILH9q4LplVIJVV_F2eb_-rVfShWK7vi8fUZIBg&oe=62BA0E7D&_nc_sid=bcb968', scheme='https', host='scontent-mxp2-1.cdninstagram.com', tld='com', host_type='domain', port='443', path='/v/t51.2885-15/11249882_966261376755731_963030927_n.jpg', query='se=8&stp=dst-jpg_e35&_nc_ht=scontent-mxp2-1.cdninstagram.com&_nc_cat=111&_nc_ohc=QeSTLR-83PoAX_ePcKi&edm=AKmAybEBAAAA&ccb=7-5&ig_cache_key=MTIyOTEzNTQ0NTAwMDU1ODY0Mg%3D%3D.2-ccb7-5&oh=00_AT90D8dLILH9q4LplVIJVV_F2eb_-rVfShWK7vi8fUZIBg&oe=62BA0E7D&_nc_sid=bcb968')}

import os, json, sys
from instagrapi import Client
import instagrapi
from typing import Dict
import pprint

proxy = 'http://96.9.71.18:33427'

os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy

def createLoggedInClient():
	client = Client()
	client.login("foxybyte.swe", "Swe_2022")
	#client.dump_settings((str(sys.path[0]))+"/data/settingsdump.json")
	#client.load_settings((str(sys.path[0]))+"/data/settingsdump.json")
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


# la politica di ordinamento per le location può essere una coda con priorità in base
# all'ultima volta che una certa location è stata analizzata

def crawlAllLocations(locationNamesList, client, nPostsWanted):
	locationsData = { }
	for loc in locationNamesList:
		mediasDump = getTopMediasFromLocation(loc, client) #returns a list of "Medias"
		formattedMediasFromLocation = []
		for media in mediasDump[0:nPostsWanted]:
			formattedMediasFromLocation.append(formatMediaToDictionaryItem(media,client)) 
		locationsData[loc] = formattedMediasFromLocation
	return locationsData


#########

#Main Function 

def beginCrawling():
	client = createLoggedInClient()
	locationNamesList = getAllCrawlableLocationsFromSomewhere()
	nPostsWanted = 2 # only get N+1 top posts from each location
	locationsData = crawlAllLocations(locationNamesList, client, nPostsWanted)
	writeCrawledDataToJson(locationsData)

###########	

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


def formatMediaToDictionaryItem(media,client): #need to serialize casting to primitive data types
	formattedDictionaryMedia = {}
	formattedDictionaryMedia["MediaType"] = getMediaType(media)
	formattedDictionaryMedia["TakenAtTime"] = parseTakenAtTime(getMediaTime(media))
	formattedDictionaryMedia["TakenAtLocation"] = parseTakenAtLocation(media,client) #extra step necessary.
	formattedDictionaryMedia["LikeCount"] = getMediaLikeCount(media)
	formattedDictionaryMedia["CaptionText"] = getCaptionText(media)
	formattedDictionaryMedia["MediaURL"] = parseMediaUrl(getMediaURL(media))
	pprint.pprint(formattedDictionaryMedia)
	return formattedDictionaryMedia


	
def getDetailedMediaLocationInfo(media, client):  # this works and retrieves all category and other data
    mediainfo = client.media_info_v1(media.pk)
    if mediainfo.location != None:
        return client.location_info((mediainfo.location).pk)
    else:
        return None


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

def main():
	beginCrawling()

################################################################

if __name__ == "__main__":
	main()


#	{'Lunaelaltro\n': [{'MediaType': 1, 
#						'TakenAtTime': datetime.datetime(2016, 4, 15, 18, 19, 44, tzinfo=datetime.timezone.utc), 
#						'TakenAtLocationName': Location(pk=3110887, name='Ristorante Pizzeria Lunaelaltro - Marostica', phone='', website='', category='', hours={}, address=None, city=None, zip=None, lng=11.660707634193, lat=45.736862428411, external_id=77610911328, external_id_source='facebook_places'), ù
#						'LikeCount': 1, 
#						'MediaURL': HttpUrl('https://scontent-mxp2-1.cdninstagram.com/v/t51.2885-15/11249882_966261376755731_963030927_n.jpg?se=8&stp=dst-jpg_e35&_nc_ht=scontent-mxp2-1.cdninstagram.com&_nc_cat=111&_nc_ohc=QeSTLR-83PoAX_ePcKi&edm=AKmAybEBAAAA&ccb=7-5&ig_cache_key=MTIyOTEzNTQ0NTAwMDU1ODY0Mg%3D%3D.2-ccb7-5&oh=00_AT90D8dLILH9q4LplVIJVV_F2eb_-rVfShWK7vi8fUZIBg&oe=62BA0E7D&_nc_sid=bcb968', scheme='https', host='scontent-mxp2-1.cdninstagram.com', tld='com', host_type='domain', port='443', path='/v/t51.2885-15/11249882_966261376755731_963030927_n.jpg', query='se=8&stp=dst-jpg_e35&_nc_ht=scontent-mxp2-1.cdninstagram.com&_nc_cat=111&_nc_ohc=QeSTLR-83PoAX_ePcKi&edm=AKmAybEBAAAA&ccb=7-5&ig_cache_key=MTIyOTEzNTQ0NTAwMDU1ODY0Mg%3D%3D.2-ccb7-5&oh=00_AT90D8dLILH9q4LplVIJVV_F2eb_-rVfShWK7vi8fUZIBg&oe=62BA0E7D&_nc_sid=bcb968')}


import os, json, sys
from instagrapi import Client
import instagrapi
from typing import Dict


def createLoggedInClient():
	client = Client()
	client.login("foxybyte.swe", "Swe_2022")
	return client

def getAllCrawlableLocationsFromSomewhere():
	txt_file = open((str(sys.path[0]))+"\\data\\locations.txt", "r")
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

def writeCrawledDataToJson(locationsData):  #TypeError: Object of type datetime is not JSON serializable
	jsondump= json.dumps(locationsData)
	with open((str(sys.path[0]))+"\\data\\locationsData.json", "a") as outfile:
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
	#writeCrawledDataToJson(locationsData)
	print(locationsData)

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
	formattedDictionaryMedia["TakenAtTime"] = getMediaTime(media)
	formattedDictionaryMedia["TakenAtLocationName"] = getMediaLocationName(media)
	formattedDictionaryMedia["LikeCount"] = getMediaLikeCount(media)
	formattedDictionaryMedia["MediaURL"] = getMediaURL(media)
	return formattedDictionaryMedia
	



# useful media keys: pk, id, code, media_type, caption_text
# from pk -> media -> method photo_download or media_info -> url or code (to add base link structure)
# or in media_info -> resources -> video_url or thumbnail_url (if photo)



#################################################################


def main():
	beginCrawling()

################################################################

if __name__ == "__main__":
    main()


#	{'Lunaelaltro\n': [{'MediaType': 1, 'TakenAtTime': datetime.datetime(2016, 4, 15, 18, 19, 44, tzinfo=datetime.timezone.utc), 'TakenAtLocationName': Location(pk=3110887, name='Ristorante Pizzeria Lunaelaltro - Marostica', phone='', website='', category='', hours={}, address=None, city=None, zip=None, lng=11.660707634193, lat=45.736862428411, external_id=77610911328, external_id_source='facebook_places'), 'LikeCount': 1, 'MediaURL': HttpUrl('https://scontent-mxp2-1.cdninstagram.com/v/t51.2885-15/11249882_966261376755731_963030927_n.jpg?se=8&stp=dst-jpg_e35&_nc_ht=scontent-mxp2-1.cdninstagram.com&_nc_cat=111&_nc_ohc=QeSTLR-83PoAX_ePcKi&edm=AKmAybEBAAAA&ccb=7-5&ig_cache_key=MTIyOTEzNTQ0NTAwMDU1ODY0Mg%3D%3D.2-ccb7-5&oh=00_AT90D8dLILH9q4LplVIJVV_F2eb_-rVfShWK7vi8fUZIBg&oe=62BA0E7D&_nc_sid=bcb968', scheme='https', host='scontent-mxp2-1.cdninstagram.com', tld='com', host_type='domain', port='443', path='/v/t51.2885-15/11249882_966261376755731_963030927_n.jpg', query='se=8&stp=dst-jpg_e35&_nc_ht=scontent-mxp2-1.cdninstagram.com&_nc_cat=111&_nc_ohc=QeSTLR-83PoAX_ePcKi&edm=AKmAybEBAAAA&ccb=7-5&ig_cache_key=MTIyOTEzNTQ0NTAwMDU1ODY0Mg%3D%3D.2-ccb7-5&oh=00_AT90D8dLILH9q4LplVIJVV_F2eb_-rVfShWK7vi8fUZIBg&oe=62BA0E7D&_nc_sid=bcb968')}















#import sys, time, os, json
#from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#
#chromedriverDirectory = "C:/Users/marco/Desktop/FoxyByte/Crawler/chromedriver.exe"  #EDIT
#profileDirectory = "C:/Users/marco/Desktop/FoxyByte/Crawler/Profile"	#EDIT
#
#def buildWebDriver():
#	chrome_options = webdriver.ChromeOptions()
#	chrome_options.add_experimental_option("useAutomationExtension", False)
#	chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#	chrome_options.add_argument("user-data-dir=" + profileDirectory)
#
#	driver = webdriver.Chrome(chromedriverDirectory, options=chrome_options)
#	return driver
#
#
#
#def getLocationPageBySearchBar(locationName, driver):
#	driver.get("https://www.instagram.com/")
#	time.sleep(3)
#
#	element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[contains(@class,'XTCLo')]")))
# 
#	time.sleep(5)
#	driver.execute_script("arguments[0].click();", element)
#	time.sleep(5)
#	element.send_keys(locationName)
#	time.sleep(2)
#
#	url_array = driver.find_elements_by_css_selector(".-qQT3")
#	
#	for url in url_array:
#		if 'explore/locations' in str(url.get_attribute('href')):
#			print(url.get_attribute('href'))	
#			return str(url.get_attribute('href'))
#
#
#
#
#def getLocationPagePosts(locationURL, driver, scroll):
#	driver.get(locationURL)
#	time.sleep(3)
#
#	screen_height = driver.execute_script("return window.screen.height;")
#	
#	if scroll==True:
#		i = 1	
#		while True:
#			driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
#			i += 1
#			time.sleep(3)
#			scroll_height = driver.execute_script("return document.body.scrollHeight;")  
#			if (screen_height) * i > scroll_height or i>2:
#				break 
#
#	posts = driver.find_elements_by_css_selector(".v1Nh3 > a")
#	url_array=[]
#	for post in posts:
#		url_array.append(post.get_attribute('href'))
#	return url_array
#
#def getPost(post, driver):
#	driver.get(post)
#
#def getPostImageSrc(url, driver):
#
#	posts = driver.find_elements_by_css_selector(".FFVAD")
#	src_data_array=[]
#	for data in posts:
#		src_data_array.append(data.get_attribute('src'))
#	post_src_array=[]
#	for src in src_data_array:
#		post_src_array.append(src)
#	return post_src_array
#
#
#def getPostDescriptionAndComments(url, driver):
#	driver.get(url)
#	time.sleep(5)
#
#	texts_list = []
#	texts = driver.find_elements_by_css_selector('.MOdxS ')
#	#print(len(texts))
#	for txt in texts:
#		texts_list.append(txt.text)
#	return texts_list
#
#
#
#
#def oldmain():
#	
#	locationName=input("Please Input the Location Name: ")
#	
#
#	driver = buildWebDriver()
#
#	locationUrl = getLocationPageBySearchBar(locationName, driver)
#	
#	locationPostsArray = getLocationPagePosts(locationUrl, driver, False)
#
#	postdata={}
#
#
#	test = locationPostsArray[0:4]	#just to test a subset of the result
#	print(test)
#	for post in test:
#			getPost(post, driver)
#			postImage = getPostImageSrc(post, driver)
#			postText = getPostDescriptionAndComments(post, driver)
#			postdata[post]= {"image": postImage, "text": postText}
#
#	
#	
#	
#	#print(postdata)
#
## LocationDictionary Structure
## 	
## Dictionary -> LocationName -> /////(locationURL (str))
#			#			     -> Posts -> PostImageSrc (str) / (array if multi-photo)
#			#			   			  -> PostText (array) with element[0] being the post description, the rest is comments
#	
#	
#	locations={}
#	locations[locationName]= postdata
#
#	jsondump= json.dumps(locations)
#	os.chdir("C:/Users/marco/Desktop/FoxyByte/Crawler/")
#	with open("locations.json", "a") as outfile:
#		outfile.write(jsondump)
#
#
#
#	sys.exit(0)
#
#
#
#
#

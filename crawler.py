import sys, time, os, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriverDirectory = "C:/Users/marco/Desktop/FoxyByte/Crawler/chromedriver.exe"  #EDIT
profileDirectory = "C:/Users/marco/Desktop/FoxyByte/Crawler/Profile"	#EDIT

def buildWebDriver():
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_experimental_option("useAutomationExtension", False)
	chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
	chrome_options.add_argument("user-data-dir=" + profileDirectory)

	driver = webdriver.Chrome(chromedriverDirectory, options=chrome_options)
	return driver



def getLocationPageBySearchBar(locationName, driver):
	driver.get("https://www.instagram.com/")
	time.sleep(3)

	element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[contains(@class,'XTCLo')]")))
 
	time.sleep(5)
	driver.execute_script("arguments[0].click();", element)
	time.sleep(5)
	element.send_keys(locationName)
	time.sleep(2)

	url_array = driver.find_elements_by_css_selector(".-qQT3")
	
	for url in url_array:
		if 'explore/locations' in str(url.get_attribute('href')):
			print(url.get_attribute('href'))	
			return str(url.get_attribute('href'))




def getLocationPagePosts(locationURL, driver, scroll):
	driver.get(locationURL)
	time.sleep(3)

	screen_height = driver.execute_script("return window.screen.height;")
	
	if scroll==True:
		i = 1	
		while True:
			driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
			i += 1
			time.sleep(3)
			scroll_height = driver.execute_script("return document.body.scrollHeight;")  
			if (screen_height) * i > scroll_height or i>2:
				break 

	posts = driver.find_elements_by_css_selector(".v1Nh3 > a")
	url_array=[]
	for post in posts:
		url_array.append(post.get_attribute('href'))
	return url_array

def getPost(post, driver):
	driver.get(post)

def getPostImageSrc(url, driver):

	posts = driver.find_elements_by_css_selector(".FFVAD")
	src_data_array=[]
	for data in posts:
		src_data_array.append(data.get_attribute('src'))
	post_src_array=[]
	for src in src_data_array:
		post_src_array.append(src)
	return post_src_array


def getPostDescriptionAndComments(url, driver):
	driver.get(url)
	time.sleep(5)

	texts_list = []
	texts = driver.find_elements_by_css_selector('.MOdxS ')
	#print(len(texts))
	for txt in texts:
		texts_list.append(txt.text)
	return texts_list


#################################################################

def main():
	
	locationName=input("Please Input the Location Name: ")
	

	driver = buildWebDriver()

	locationUrl = getLocationPageBySearchBar(locationName, driver)
	
	locationPostsArray = getLocationPagePosts(locationUrl, driver, False)

	postdata={}


	test = locationPostsArray[0:4]	#just to test a subset of the result
	print(test)
	for post in test:
			getPost(post, driver)
			postImage = getPostImageSrc(post, driver)
			postText = getPostDescriptionAndComments(post, driver)
			postdata[post]= {"image": postImage, "text": postText}

	
	
	
	#print(postdata)

# LocationDictionary Structure
# 	
# Dictionary -> LocationName -> /////(locationURL (str))
			#			     -> Posts -> PostImageSrc (str) / (array if multi-photo)
			#			   			  -> PostText (array) with element[0] being the post description, the rest is comments
	
	
	locations={}
	locations[locationName]= postdata

	jsondump= json.dumps(locations)
	os.chdir("C:/Users/marco/Desktop/FoxyByte/Crawler/")
	with open("locations.json", "a") as outfile:
		outfile.write(jsondump)



	sys.exit(0)


################################################################

if __name__ == "__main__":
    main()
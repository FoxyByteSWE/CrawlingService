import os, json, sys, time
from pprint import pprint
from instagrapi import Client
import instagrapi
from typing import Dict
from abc import ABC, abstractmethod

from InstagrapiUtils import InstagrapiUtils

#proxy = 'http://46.105.142.10:7497'

#os.environ['http_proxy'] = proxy 
#os.environ['HTTP_PROXY'] = proxy
#os.environ['https_proxy'] = proxy
#os.environ['HTTPS_PROXY'] = proxy



class WriteJSONStrategy(ABC):
	@abstractmethod
	def writeToJSON(self, data):
		pass


class UsersWriteJSONStrategy(WriteJSONStrategy):
	def writeToJSON(self, data): #writenewuserstojsonfile
		jsondump= json.dumps(data)
		with open((str(sys.path[0]))+"/data/trackedUsers.json", "w") as outfile:
			outfile.write(jsondump)	

class TrackedLocationsWriteJSONStrategy(WriteJSONStrategy):
	def writeToJSON(self, data): #writenewuserstojsonfile
		jsondump= json.dumps(data)
		with open((str(sys.path[0]))+"/data/locations.json", "w") as outfile:
			outfile.write(jsondump)


class ReadJSONStrategy(ABC):
	@abstractmethod
	def readFromJSON(self):
		pass



class TrackedLocationsReadJSONStrategy(ReadJSONStrategy):
	def readFromJSON(self):
		filepath = (str(sys.path[0]))+"/data/locations.json"
		with open(filepath) as locationsFile:
			try:
				data = json.load(locationsFile)
				return data
			except Exception as e:
				print(e)
				return {}


class UsersReadJSONStrategy(ReadJSONStrategy):
	def readFromJSON(self):
		filepath = (str(sys.path[0]))+"/data/trackedUsers.json"
		with open(filepath) as usersFile:
			try:
				data = json.load(usersFile)
				return data
			except Exception as e:
				print(e)
				return {}





class ProfileScraper:


	def readFromJSON(self, processing_strategy: ReadJSONStrategy):
		return processing_strategy.readFromJSON()

	def writeToJSON(self, data, processing_strategy: WriteJSONStrategy):
		return processing_strategy.writeToJSON(data)

#	def getTrackedLocationsFromJSON():
#		filepath = (str(sys.path[0]))+"/data/locations.json"
#		with open(filepath) as locationsFile:
#			try:
#				data = json.load(locationsFile)
#				return data
#			except Exception as e:
#				print(e)
#				return None


#	def writeLocationsToJSON(locations): 
#		jsondump= json.dumps(locations)
#		with open((str(sys.path[0]))+"/data/locations.json", "w") as outfile:
#			outfile.write(jsondump)


	def trackLocation(self, locationdict):
		locationsFromJSON = self.readFromJSON(TrackedLocationsReadJSONStrategy)
		print("tracking location: "+ locationdict["name"])
		locationsFromJSON[locationdict["pk"]]=locationdict
		#ProfileScraper.writeLocationsToJSON(locationsFromJSON)
		self.writeToJSON(locationsFromJSON, TrackedLocationsWriteJSONStrategy)



#	def writeNewUsersToJSONFile(newusers):
#		jsondump= json.dumps(newusers)
#		with open((str(sys.path[0]))+"/data/trackedUsers.json", "w") as outfile:
#			outfile.write(jsondump)
#
#
#	def getTrackedUsersFromJSON():
#		filepath = (str(sys.path[0]))+"/data/trackedUsers.json"
#		with open(filepath) as usersFile:
#			try:
#				data = json.load(usersFile)
#				return data
#			except Exception as e:
#				print(e)
#				return None



	def isLocationTracked(self, location):
		#data = ProfileScraper.getTrackedLocationsFromJSON()
		data = self.readFromJSON(TrackedLocationsReadJSONStrategy)
		if location.pk in data:
			return True
		else:
			return False



	def createLocation(input, coordinates):
		dict = {}
		#dict["LastChecked"]=0 # decomment this in order for time-based queueing to work
		dict["pk"] = input["pk"]
		dict["name"] = input["name"]
		dict["address"] = input["address"]
		dict["coordinates"] = [coordinates["lng"], coordinates["lat"]]
		dict["category"] = input["category"]
		dict["phone"] = input["phone"]
		dict["website"] = input["website"]
		return dict;

	def getMediaLocationCoordinates(media):
		coordinates = {'lng': (media.location).lng , 
						'lat': (media.location).lat }
		return coordinates








	def isAlreadyTracked(self, user): #check if database or file already contains this user
		#data = ProfileScraper.getTrackedUsersFromJSON()
		data = self.readFromJSON(UsersReadJSONStrategy)
		#print(data)
		if user.username in data:
			return True
		else:
			return False


	def trackUser(self, user, client):
		#=(client.user_info(user.pk)).username
		#username = client.user_info_by_username_v1(username).pk
		username = user.username
		#usersfromjson = ProfileScraper.getTrackedUsersFromJSON()
		usersfromjson = self.readFromJSON(UsersReadJSONStrategy)
		print("tracking user: "+ username)
		usersfromjson[username]=user.dict()
		#ProfileScraper.writeNewUsersToJSONFile(usersfromjson)
		self.writeToJSON(usersfromjson, UsersWriteJSONStrategy)






	################

	# EXTEND USERS POOL

	def extendFollowingUsersPoolFromSuggested(userid, client, limit):
		try:
			list = InstagrapiUtils.getSuggestedUsersFromFBSearch(userid, client)
		except Exception as e:
			print(e)
			return
		for usersh in list[0:limit]:
			user = InstagrapiUtils.getUserInfoByUsername((InstagrapiUtils.convertUserShortToUserv2(usersh, client).username),client)
			if InstagrapiUtils.isProfilePrivate(user) == False:
				if ProfileScraper.isAlreadyTracked(user) == False:
					ProfileScraper.trackUser(user, client)


	def extendFollowingUsersPoolFromPostTaggedUsers(post,client):
		list = InstagrapiUtils.getPostTaggedPeople(post)
		for usertag in list:
			usersh=InstagrapiUtils.convertUsertagToUser(usertag)
			user = InstagrapiUtils.etUserInfoByUsername((InstagrapiUtils.convertUserShortToUser(usersh, client).username),client)
			if InstagrapiUtils.isProfilePrivate(user) == False:
				if ProfileScraper.isAlreadyTracked(user) == False:
					ProfileScraper.trackUser(user, client)



	def extendFollowingUsersPoolFromTaggedPostsSection(userid, client, limit):
		list = InstagrapiUtils.getProfileTaggedPosts(userid, client)
		for media in list[0:limit]:
			user=InstagrapiUtils.getUserInfoByUsername(InstagrapiUtils.getUsernameFromID(userid,client),client)
			if ProfileScraper.isAlreadyTracked(user) == False:
				if InstagrapiUtils.isProfilePrivate(user) == False:
						ProfileScraper.trackUser(user, client)



	#####################

	# FIND RESTAURANTS

	def crawlRestaurantsFromProfilePosts(userid, client, allowExtendUserBase, nPostsAllowed):

		restaurant_tags = ['Restaurant', 'Italian Restaurant','Pub', 'Bar', 'Grocery ', 'Wine', 'Diner', 'Food', 'Meal', 'Breakfast', 'Lunch',
							'Dinner', 'Cafe', 'Tea Room', 'Hotel', 'Pizza', 'Coffee', 'Bakery', 'Dessert', 'Gastropub',
							'Sandwich', 'Ice Cream', 'Steakhouse', 'Pizza place', 'Fast food restaurant', 'Deli']

		postlist = InstagrapiUtils.getUserPosts(userid, client)
		if nPostsAllowed > len(postlist):
			nPostsAllowed = len(postlist)
		for post in postlist[0:nPostsAllowed]:
			if InstagrapiUtils.hasTaggedLocation(post):
				detailedLocationInfo = InstagrapiUtils.getDetailedMediaLocationInfo(post, client)
				#print("location is a: "+str(detailedLocationInfo.category))
				if detailedLocationInfo.category in restaurant_tags and ProfileScraper.isLocationTracked(detailedLocationInfo)==False:
					coordinates = ProfileScraper.getMediaLocationCoordinates(post)
					ProfileScraper.trackLocation(ProfileScraper.createLocation(detailedLocationInfo.dict(), coordinates))
			
			if allowExtendUserBase and InstagrapiUtils.getPostTaggedPeople(post) != []:
				#print("Now extending User Base")
				#print(getPostTaggedPeople(post))
				ProfileScraper.extendFollowingUsersPoolFromPostTaggedUsers(post, client)
				#print("Finished Extending User Base")




#########################



#################################################################

def main():
	
	# Settings can be fetched through a JSON Config File

	allowExtendUserBase = True   
	nPostsAllowed = 40

	client = InstagrapiUtils.createLoggedInClient()
	trackedUsers = ProfileScraper.getTrackedUsersFromJSON()	 
	#trackedUsers = ["marcouderzo"] #tests from our account's posts.
	
	for user in trackedUsers:
		print("MAIN LOOP: " + str(user))
		userid = InstagrapiUtils.getUserIDfromUsername(user, client)
		ProfileScraper.crawlRestaurantsFromProfilePosts(userid, client, allowExtendUserBase, nPostsAllowed)
		if allowExtendUserBase:
			#print("Now extending User  (from main)")
			ProfileScraper.extendFollowingUsersPoolFromTaggedPostsSection(userid, client, 4)
			ProfileScraper.extendFollowingUsersPoolFromSuggested(userid, client, 4)
			#print("Finished Extending User Base (from main)")
		



################################################################

if __name__ == "__main__":
	main()

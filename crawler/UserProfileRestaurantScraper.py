import os, json, sys, time
from pprint import pprint
from instagrapi import Client
import instagrapi
from typing import Dict
from abc import ABC, abstractmethod

from InstagrapiUtils import InstagrapiUtils
from JSONUtils import JSONUtils
from Config import CrawlingServiceConfig

#proxy = 'http://46.105.142.10:7497'

#os.environ['http_proxy'] = proxy 
#os.environ['HTTP_PROXY'] = proxy
#os.environ['https_proxy'] = proxy
#os.environ['HTTPS_PROXY'] = proxy



class ProfileScraper:

	jsonUtils = JSONUtils()
	instagrapiUtils = InstagrapiUtils()


	def readFromJSON(processing_strategy: JSONUtils.ReadJSONStrategy):
		return processing_strategy.readFromJSON()

	def writeToJSON(data, processing_strategy: JSONUtils.WriteJSONStrategy):
		return processing_strategy.writeToJSON(data)


	def trackLocation(self, locationdict):
		locationsFromJSON = self.readFromJSON(JSONUtils.TrackedLocationsReadJSONStrategy)
		print("tracking location: "+ locationdict["name"])
		locationsFromJSON[locationdict["pk"]]=locationdict
		#ProfileScraper.writeLocationsToJSON(locationsFromJSON)
		self.writeToJSON(locationsFromJSON, JSONUtils.TrackedLocationsWriteJSONStrategy)


	def isLocationTracked(self, location):
		#data = ProfileScraper.getTrackedLocationsFromJSON()
		data = self.readFromJSON(JSONUtils.TrackedLocationsReadJSONStrategy)
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
		data = self.readFromJSON(JSONUtils.UsersReadJSONStrategy)
		#print(data)
		if user.username in data:
			return True
		else:
			return False


	def trackUser(self, user):
		#username = client.user_info_by_username_v1(username).pk
		username = user.username
		usersfromjson = self.readFromJSON(JSONUtils.UsersReadJSONStrategy)
		print("tracking user: "+ username)
		usersfromjson[username]=user.dict()
		self.writeToJSON(usersfromjson, JSONUtils.UsersWriteJSONStrategy)






	################

	# EXTEND USERS POOL

	def extendFollowingUsersPoolFromSuggested(self, userid, limit):
		try:
			list = self.instagrapiUtils.getSuggestedUsersFromFBSearch(userid)
		except Exception as e:
			print(e)
			return
		for usersh in list[0:limit]:
			user = self.instagrapiUtils.getUserInfoByUsername((self.instagrapiUtils.convertUserShortToUserv2(usersh).username))
			user["LatestPostPartialURL"] = self.instagrapiUtils.getLatestPostPartialURL(userid)
			if self.instagrapiUtils.isProfilePrivate(user) == False:
				if self.isAlreadyTracked(user) == False:
					self.trackUser(user)


	def extendFollowingUsersPoolFromPostTaggedUsers(self,post):
		list = self.instagrapiUtils.getPostTaggedPeople(post)
		for usertag in list:
			usersh=self.instagrapiUtils.convertUsertagToUser(usertag)
			user = self.instagrapiUtils.GetUserInfoByUsername((self.instagrapiUtils.convertUserShortToUser(usersh).username))
			user["LatestPostPartialURL"] = self.instagrapiUtils.getLatestPostPartialURL(user.pk)
			if self.instagrapiUtils.isProfilePrivate(user) == False:
				if self.isAlreadyTracked(user) == False:
					self.trackUser(user)



	def extendFollowingUsersPoolFromTaggedPostsSection(self, userid, limit):
		list = self.instagrapiUtils.getProfileTaggedPosts(userid)
		for media in list[0:limit]:
			user=self.instagrapiUtils.getUserInfoByUsername(self.instagrapiUtils.getUsernameFromID(userid))
			user["LatestPostPartialURL"] = self.instagrapiUtils.getLatestPostPartialURL(userid)
			if self.isAlreadyTracked(user) == False:
				if self.instagrapiUtils.isProfilePrivate(user) == False:
						self.trackUser(user)


	def updateUserLatestPostPartialURL(self, userid, latestPURL):
		users = self.readFromJSON(JSONUtils.UsersReadJSONStrategy)
		targetuser = users[userid]
		targetuser["LatestPostPartialURL"] = latestPURL
		users[userid] = targetuser
		self.writeToJSON(users, JSONUtils.UsersWriteJSONStrategy)

	
	def checkIfPostIsNew(indexedPURL, latestPURL):
		if latestPURL == indexedPURL:
			return False
		else:
			return True
		
		
		
	#####################

	# FIND RESTAURANTS

	def crawlRestaurantsFromProfilePosts(self, userid, allowExtendUserBase, nPostsAllowed):

		restaurant_tags = ['Restaurant', 'Italian Restaurant','Pub', 'Bar', 'Grocery ', 'Wine', 'Diner', 'Food', 'Meal', 'Breakfast', 'Lunch',
							'Dinner', 'Cafe', 'Tea Room', 'Hotel', 'Pizza', 'Coffee', 'Bakery', 'Dessert', 'Gastropub',
							'Sandwich', 'Ice Cream', 'Steakhouse', 'Pizza place', 'Fast food restaurant', 'Deli']

		postlist = self.instagrapiUtils.getUserPosts(userid)
		if nPostsAllowed > len(postlist):
			nPostsAllowed = len(postlist)
		latestPURL = self.instagrapiUtils.getLatestPostPartialURL(userid)
		if self.isAlreadyTracked(userid):
			self.updateUserLatestPostPartialURL(userid, latestPURL) #needs user
		for post in postlist[0:nPostsAllowed]:


			if self.checkIfPostIsNew(self.instagrapiUtils.getPostPartialURL(post), latestPURL) == False:  # check if reached a post already checked before.
				# no need to go on
				return


			if self.instagrapiUtils.hasTaggedLocation(post):
				detailedLocationInfo = self.instagrapiUtils.getDetailedMediaLocationInfo(post)
				#print("location is a: "+str(detailedLocationInfo.category))
				if detailedLocationInfo.category in restaurant_tags and self.isLocationTracked(detailedLocationInfo)==False:
					coordinates = self.getMediaLocationCoordinates(post)
					self.trackLocation(self.createLocation(detailedLocationInfo.dict(), coordinates))
			
			if allowExtendUserBase and self.instagrapiUtils.getPostTaggedPeople(post) != []:
				#print("Now extending User Base")
				#print(getPostTaggedPeople(post))
				self.extendFollowingUsersPoolFromPostTaggedUsers(post)
				#print("Finished Extending User Base")


	def beginScraping(self, allowExtendUserBase, nPostsAllowed):
		
		trackedUsers = ProfileScraper.readFromJSON(JSONUtils.UsersReadJSONStrategy())
		#trackedUsers = ["marcouderzo"] #tests from our account's posts.
		
		for user in trackedUsers:
			print("MAIN LOOP: " + str(user))
			userid = self.instagrapiUtils.getUserIDfromUsername(user)
			ProfileScraper.crawlRestaurantsFromProfilePosts(userid, allowExtendUserBase, nPostsAllowed)
			if allowExtendUserBase:
				#print("Now extending User  (from main)")
				ProfileScraper.extendFollowingUsersPoolFromTaggedPostsSection(userid, 4)
				ProfileScraper.extendFollowingUsersPoolFromSuggested(userid, 4)
				#print("Finished Extending User Base (from main)")

#########################



#################################################################
#
#def main():
#	
#	# Settings can be fetched through a JSON Config File
#
#	config = CrawlingServiceConfig()
#
#	allowExtendUserBase = config.allowExtendUserBase 
#	nPostsAllowed = config.nPostsAllowedForProfileScraping
#
#	client = self.instagrapiUtils.createLoggedInClient()
#	trackedUsers = ProfileScraper.readFromJSON(JSONUtils.UsersReadJSONStrategy())
#	#trackedUsers = ["marcouderzo"] #tests from our account's posts.
#	
#	for user in trackedUsers:
#		print("MAIN LOOP: " + str(user))
#		userid = self.instagrapiUtils.getUserIDfromUsername(user, client)
#		ProfileScraper.crawlRestaurantsFromProfilePosts(userid, client, allowExtendUserBase, nPostsAllowed)
#		if allowExtendUserBase:
#			#print("Now extending User  (from main)")
#			ProfileScraper.extendFollowingUsersPoolFromTaggedPostsSection(userid, client, 4)
#			ProfileScraper.extendFollowingUsersPoolFromSuggested(userid, client, 4)
#			#print("Finished Extending User Base (from main)")
#		
#
#
#
################################################################

#if __name__ == "__main__":
	#main()

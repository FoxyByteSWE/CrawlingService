import os, json, sys, time
from pprint import pprint
from instagrapi import Client
import instagrapi
from abc import ABC, abstractmethod

from InstagrapiUtils import InstagrapiUtils
from JSONUtils import JSONUtils
from Config import CrawlingServiceConfig


class ProfileScraper:

	jsonUtils = JSONUtils()
	instagrapiUtils = InstagrapiUtils()


	def readFromJSON(self, processing_strategy: JSONUtils.ReadJSONStrategy):
		return processing_strategy.readFromJSON(self)

	def writeToJSON(self, data, processing_strategy: JSONUtils.WriteJSONStrategy):
		return processing_strategy.writeToJSON(self, data)


	def trackLocation(self, locationdict) -> None:
		locationsFromJSON = self.readFromJSON(JSONUtils.TrackedLocationsReadJSONStrategy)
		print("tracking location: "+ locationdict["name"])
		locationsFromJSON[locationdict["pk"]]=locationdict
		self.writeToJSON(locationsFromJSON, JSONUtils.TrackedLocationsWriteJSONStrategy)


	def isLocationTracked(self, location) -> bool:
		data = self.readFromJSON(JSONUtils.TrackedLocationsReadJSONStrategy)
		print(data.keys())
		if str(location.pk) in data.keys():
			
			print("location is already being tracked.")
			return True
		else:
			return False



	def createLocation(self, input, coordinates) -> dict:
		dict = {}
		dict["pk"] = input["pk"]
		dict["name"] = input["name"]
		dict["address"] = input["address"]
		dict["coordinates"] = [coordinates["lng"], coordinates["lat"]]
		dict["category"] = input["category"]
		dict["phone"] = input["phone"]
		dict["website"] = input["website"]
		return dict;

	def getMediaLocationCoordinates(self, media) -> dict:
		coordinates = {'lng': (media.location).lng , 
						'lat': (media.location).lat }
		return coordinates


	def isAlreadyTracked(self, user: dict) -> bool: #check if database or file already contains this user
		#data = ProfileScraper.getTrackedUsersFromJSON()
		data = self.readFromJSON(JSONUtils.UsersReadJSONStrategy)
		#print(data)
		if user.get('username') in data:
			return True
		else:
			return False


	def trackUser(self, user: dict) -> None:
		#username = client.user_info_by_username_v1(username).pk
		username = user.get('username')
		usersfromjson = self.readFromJSON(JSONUtils.UsersReadJSONStrategy)
		print("tracking user: "+ username)
		usersfromjson[username]=user#.dict()
		self.writeToJSON(usersfromjson, JSONUtils.UsersWriteJSONStrategy)






	################

	# EXTEND USERS POOL

	def extendFollowingUsersPoolFromSuggested(self, user: dict, limit: int) -> None:
		try:
			list = self.instagrapiUtils.getSuggestedUsersFromFBSearch(user)
		except Exception as e:
			print(e)
			return
		if limit > len(list):
			limit = len(list)
		for usersh in list[0:limit]:
			usertmp = self.instagrapiUtils.convertUserShortToUserv2(usersh)
			username = usertmp.username
			usersugg = self.instagrapiUtils.getUserInfoByUsername(username).dict()
			usersugg["LatestPostPartialURL"] = ''
			if self.instagrapiUtils.isProfilePrivate(usersugg) == False:
				if self.isAlreadyTracked(usersugg) == False:
					self.trackUser(usersugg)


	def extendFollowingUsersPoolFromPostTaggedUsers(self,user: dict) -> None:
		posts = self.instagrapiUtils.getUserPosts(user)
		for post in posts:
			list = self.instagrapiUtils.getPostTaggedPeople(post)
			for usertag in list:
				usersh=self.instagrapiUtils.convertUsertagToUser(usertag)
				usertagged = (self.instagrapiUtils.getUserInfoByUsername(usersh.username)).dict()
				#usertagged = (self.instagrapiUtils.GetUserInfoByUsername(usersh.username)).dict()
				user["LatestPostPartialURL"] = ''
				if self.instagrapiUtils.isProfilePrivate(usertagged) == False:
					if self.isAlreadyTracked(usertagged) == False:
						self.trackUser(usertagged)



	def extendFollowingUsersPoolFromTaggedPostsSection(self, user: dict, limit: int) -> None:
		list = self.instagrapiUtils.getProfileTaggedPosts(user)
		if list == []:
			print("No posts available in Tagged Posts Section")
		for media in list[0:limit]:
			userposter=self.instagrapiUtils.getUserInfoByUsername(media.user.username).dict()
			user["LatestPostPartialURL"] = ''
			if self.isAlreadyTracked(userposter) == False:
				if self.instagrapiUtils.isProfilePrivate(userposter) == False:
						self.trackUser(userposter)


	def updateUserLatestPostPartialURL(self, user: dict, latestPURL: str) -> None:
		users = self.readFromJSON(JSONUtils.UsersReadJSONStrategy)
		targetuser = users[user.get('username')]
		targetuser["LatestPostPartialURL"] = latestPURL
		users[user.get('username')] = targetuser
		self.writeToJSON(users, JSONUtils.UsersWriteJSONStrategy)

	
	def checkIfPostIsNew(self, indexedPURL: str, latestPURL: str) -> bool:
		if latestPURL == indexedPURL:
			return False
		else:
			return True
		
		
		
	#####################

	# FIND RESTAURANTS

	def crawlRestaurantsFromProfilePosts(self, user: dict, nPostsAllowed: int) -> None:

		restaurant_tags = ['Restaurant', 'Italian Restaurant','Pub', 'Bar', 'Grocery ', 'Wine', 'Diner', 'Food', 'Meal', 'Breakfast', 'Lunch',
							'Dinner', 'Cafe', 'Tea Room', 'Hotel', 'Pizza', 'Coffee', 'Bakery', 'Dessert', 'Gastropub',
							'Sandwich', 'Ice Cream', 'Steakhouse', 'Pizza place', 'Fast food restaurant', 'Deli']

		postlist = self.instagrapiUtils.getUserPosts(user).dict()
		if nPostsAllowed > len(postlist):
			nPostsAllowed = len(postlist)

		latestCheckedPURL = self.instagrapiUtils.getLatestPostPartialURLChecked(user)
		for post in postlist[0:nPostsAllowed]:
			indexedPURL = self.instagrapiUtils.getPostPartialURL(post)
			if self.checkIfPostIsNew(indexedPURL, latestCheckedPURL) == False:  # check if reached a post already checked before
				return

			if self.isAlreadyTracked(user):
				self.updateUserLatestPostPartialURL(user, indexedPURL) 


			if self.instagrapiUtils.hasTaggedLocation(post):
				detailedLocationInfo = self.instagrapiUtils.getDetailedMediaLocationInfo(post)
				print("post location is a: "+str(detailedLocationInfo.category))
				if detailedLocationInfo.category in restaurant_tags and self.isLocationTracked(detailedLocationInfo)==False:
					coordinates = self.getMediaLocationCoordinates(post)
					self.trackLocation(self.createLocation(detailedLocationInfo.dict(), coordinates))

		
		


	def beginScraping(self, allowExtendUserBase: bool, nPostsAllowed: int) -> None:
		
		trackedUsers = self.readFromJSON(JSONUtils.UsersReadJSONStrategy)

		if trackedUsers == {}:
			print("here")
			kickoffUser = (self.instagrapiUtils.getUserInfoByUsername("foxybyte.swe"))
			self.extendFollowingUsersPoolFromSuggested(kickoffUser, 5)
			trackedUsers = self.readFromJSON(JSONUtils.UsersReadJSONStrategy)
		
		for user in trackedUsers.values():
			print("MAIN LOOP: " + str(user.get('username')))

			self.crawlRestaurantsFromProfilePosts(user, 25)

			if allowExtendUserBase:
				print(" ===== Starting ExtendUsersPool referencing user: " + str(user.get('username')) + " =====")
				#print("Extending by Suggested Users of user: " + str(user.get('username')))
				#self.extendFollowingUsersPoolFromSuggested(user, 5) #follow up to N new users. This throws an internal instagrapi Exception
				print("Extending From Tagged Posts Section of user: " + str(user.get('username')))
				self.extendFollowingUsersPoolFromTaggedPostsSection(user, nPostsAllowed)  #follows all possible users 
				print("Extending From Users Tagged in Posts of user: " + str(user.get('username')))
				self.extendFollowingUsersPoolFromPostTaggedUsers(user) #follows all possible users 

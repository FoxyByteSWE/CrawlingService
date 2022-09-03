import os, json, sys, time
from pprint import pprint
from instagrapi import Client
import instagrapi
from abc import ABC, abstractmethod

from InstagrapiUtils import InstagrapiUtils
from JSONUtils import JSONUtils
from Config import CrawlingServiceConfig
from location.Location import Location
from location.LocationFactory import LocationFactory
from LocationProfileFinder import LevenshteinLocationProfileFinder 
from user.UserProfile import UserProfile
from DBConnection import DBConnection


class ProfileScraper:

	def __init__(self) -> None:
		self.jsonUtils = JSONUtils()
		self.instagrapiUtils = InstagrapiUtils()
		self.db = DBConnection()



	def trackLocation(self, location: Location) -> None:
		print("tracking location: "+ location.name)
		self.db.insertRestaurants(location)

		

	def isLocationTracked(self, location: Location) -> bool:
		query = "SELECT * FROM LOCATIONS WHERE Codice_Pk IS " + str(location.pk)
		response = self.db.executeQuery(query)
		if response != None:
			print("location is already being tracked.")
			return True
		else:
			return False


	def isAlreadyTracked(self, user: UserProfile) -> bool: #check if database or file already contains this user
		#data = ProfileScraper.getTrackedUsersFromJSON()
		query = "SELECT * FROM LOCATIONS WHERE Username IS " + str(user.username)
		response = self.db.executeQuery(query)
		if response != None:
			print("user is already being tracked.")
			return True
		else:
			return False

	def trackUser(self, user: UserProfile) -> None:
		#username = client.user_info_by_username_v1(username).pk
		self.db.insertUser(user)






	################

	# EXTEND USERS POOL

	def extendFollowingUsersPoolFromSuggested(self, user: dict, limit: int) -> None:
		try:
			list = self.instagrapiUtils.getSuggestedUsersFromFBSearch(user.pk)
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


#	def updateUserLatestPostPartialURL(self, user: dict, latestPURL: str) -> None:
#		users = self.readFromJSON(JSONUtils.UsersReadJSONStrategy)
#		targetuser = users[user.get('username')]
#		targetuser["LatestPostPartialURL"] = latestPURL
#		users[user.get('username')] = targetuser
#		self.writeToJSON(users, JSONUtils.UsersWriteJSONStrategy)

	
	def checkIfPostIsNew(self, indexedPURL: str, latestPURL: str) -> bool:
		if latestPURL == indexedPURL:
			return False
		else:
			return True
		
		
		
	#####################

	# FIND Trackable Places

	def crawlPlacesFromProfilePosts(self, user: UserProfile, nPostsAllowed: int, places_tags: list) -> None:

		postlist = self.instagrapiUtils.getUserPosts(user.pk, nPostsAllowed)

		lastpostcodechecked = user.getLastPostCheckedCode()

		for post in postlist:
			if self.checkIfPostIsNew(post.code, lastpostcodechecked) == False:  # check if reached a post already checked before
				return


			if self.instagrapiUtils.hasTaggedLocation(post):
				detailedLocationInfo = self.instagrapiUtils.getDetailedMediaLocationInfo(post)
				print("post location is a: "+str(detailedLocationInfo.category))
				if detailedLocationInfo.category in places_tags and self.isLocationTracked(detailedLocationInfo)==False:
					
					#TODO: check for its profile in location posts. if not found, discard
					locmedias = self.instagrapiUtils.getMostRecentMediasFromLocation(detailedLocationInfo.name)
					for media in locmedias:
						#search through and use locationprofilefinder distance to find name of restaurant in posters.
						if LevenshteinLocationProfileFinder.checkForRestaurantUsername(media.user.username, detailedLocationInfo.name) == True:
							profilePic = self.parseMediaUrl(self.instagrapiUtils.client.user_info_by_username(media.user.username).profile_pic_url)
							coordinates = self.instagrapiUtils.getMediaLocationCoordinates(post)
							newlocation = LocationFactory.buildLocationFromInstagrapi(detailedLocationInfo, profilePic, coordinates, "")
							self.trackLocation(newlocation)
							break
			
		if self.isAlreadyTracked(user):
			user.setLastPostCheckedCode(postlist[0].pk)

		
		

	def createKickoffUser(self):
			kickoffUser = (self.instagrapiUtils.getUserInfoByUsername("foxybyte.swe"))
			self.extendFollowingUsersPoolFromSuggested(kickoffUser, 5)

	def extendUserBase(policy):
				print(" ===== Starting ExtendUsersPool referencing user: " + str(user.get('username')) + " =====")
				#print("Extending by Suggested Users of user: " + str(user.get('username')))
				#self.extendFollowingUsersPoolFromSuggested(user, 5) #follow up to N new users. This throws an internal instagrapi Exception
				print("Extending From Tagged Posts Section of user: " + str(user.get('username')))
				self.extendFollowingUsersPoolFromTaggedPostsSection(user, nPostsAllowed)  #follows all possible users 
				print("Extending From Users Tagged in Posts of user: " + str(user.get('username')))
				self.extendFollowingUsersPoolFromPostTaggedUsers(user) #follows all possible users 
		





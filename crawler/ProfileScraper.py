import os, json, sys, time
from pprint import pprint
from instagrapi import Client
from instagrapi import types
from abc import ABC, abstractmethod

from InstagrapiUtils import InstagrapiUtils
from Config import CrawlingServiceConfig
from location.Location import Location
from location.LocationFactory import LocationFactory
from LocationProfileFinder import LocationProfileFinder 
from user.UserProfile import UserProfile
from DBConnection import DBConnection
from UserBaseExtender import UserBaseExtender


class ProfileScraper:

	def __init__(self) -> None:
		self.instagrapiUtils = InstagrapiUtils()
		self.db = DBConnection()
		self.policies = {1 : UserBaseExtender.ExtendUserBaseBySuggestedUsers,
						 2 : UserBaseExtender.ExtendUserBaseByTaggedPostsSection,
						 3 : UserBaseExtender.ExtendUserBaseByTaggedUsers}




	def extendUserBaseByPolicy(self, user, limit, processing_strategy: UserBaseExtender.ExtendUserBasePolicy) -> list[UserProfile]:
		return processing_strategy.extendUserBaseByPolicy(self, user, limit)



	def trackLocation(self, location: Location) -> None:
		print("tracking location: "+ location.name)
		self.db.insertItem(location.convertToDict())

		

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
		self.db.insertItem(user.convertToDict())


	def untrackUser(self, user: UserProfile) -> None:
		self.db.removeUser(user.convertToDict())


	def checkIfPostIsNew(self, indexedPURL: str, latestPURL: str) -> bool:
		if latestPURL == indexedPURL:
			return False
		else:
			return True
		
		
		
	#####################

	# FIND Trackable Places

	def crawlLocationsFromProfilePosts(self, user: UserProfile, nPostsAllowed: int, places_tags: list) -> None:

		keepUser = False
		postlist = self.instagrapiUtils.getUserPosts(user.pk, nPostsAllowed)

		lastpostcodechecked = user.getLastPostCheckedCode()

		for post in postlist:
			if self.checkIfPostIsNew(post.code, lastpostcodechecked) == False:  # check if reached a post already checked before
				return


			if self.instagrapiUtils.hasTaggedLocation(post):
				detailedLocationInfo = self.instagrapiUtils.getDetailedMediaLocationInfo(post)
				print("post location is a: "+str(detailedLocationInfo.category))
				if detailedLocationInfo.category in places_tags and self.isLocationTracked(detailedLocationInfo)==False:

					locmedias = self.instagrapiUtils.getMostRecentMediasFromLocation(detailedLocationInfo.name)

					mediafound = LocationProfileFinder.getMediaOfLocationUserProfileIfExists(locmedias, detailedLocationInfo.name)
					if mediafound != None:
						coordinates = self.instagrapiUtils.getMediaLocationCoordinates(post)
						profilePic = self.instagrapiUtils.parseMediaUrl(self.instagrapiUtils.client.user_info_by_username(mediafound.user.username).profile_pic_url)
						newlocation = LocationFactory.buildFromInstagrapi(detailedLocationInfo, profilePic, coordinates, "")
						self.trackLocation(newlocation)
						keepUser=True

		
		if keepUser == False:
			self.untrackUser(user)
		else:
			user.setLastPostCheckedCode(postlist[0].pk)

		
		

	def findKickoffUsers(self):
			kickoffUser = (self.instagrapiUtils.getUserInfoByUsername("foxybyte.swe"))
			newusers = self.extendUserBaseByPolicy(kickoffUser, 5, UserBaseExtender.ExtendUserBaseBySuggestedUsers)		
			for u in newusers:
				self.db.insertItem(u.convertToDict())





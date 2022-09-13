import os, json, sys, time
from pprint import pprint
from instagrapi import Client
import instagrapi
from abc import ABC, abstractmethod

from InstagrapiUtils import InstagrapiUtils
from Config import CrawlingServiceConfig
from location.Location import Location
from location.LocationFactory import LocationFactory
from LocationProfileFinder import LocationProfileFinder 
from user.UserProfile import UserProfile
from DBConnection import DBConnection


class ProfileScraper:

	def __init__(self) -> None:
		self.instagrapiUtils = InstagrapiUtils()
		self.db = DBConnection()



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


	def checkIfPostIsNew(self, indexedPURL: str, latestPURL: str) -> bool:
		if latestPURL == indexedPURL:
			return False
		else:
			return True
		
		
		
	#####################

	# FIND Trackable Places

	def crawlLocationsFromProfilePosts(self, user: UserProfile, nPostsAllowed: int, places_tags: list) -> None:

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
						profilePic = self.parseMediaUrl(self.instagrapiUtils.client.user_info_by_username(mediafound.user.username).profile_pic_url)
						newlocation = LocationFactory.buildLocationFromInstagrapi(detailedLocationInfo, profilePic, coordinates, "")
						self.trackLocation(newlocation)
			
		if self.isAlreadyTracked(user): #this should not be necessary as user comes from DB to begin with
			user.setLastPostCheckedCode(postlist[0].pk)

		
		

	def findKickoffUsers(self):
			kickoffUser = (self.instagrapiUtils.getUserInfoByUsername("foxybyte.swe"))
			self.extendFollowingUsersPoolFromSuggested(kickoffUser, 5)

	def extendUserBase(policy):
		pass
		





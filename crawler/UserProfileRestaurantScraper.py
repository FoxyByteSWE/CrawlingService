from cProfile import Profile
import os, json, sys, time
from pprint import pprint
from instagrapi import Client
import instagrapi
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


	def readFromJSON(self, processing_strategy: JSONUtils.ReadJSONStrategy):
		return processing_strategy.readFromJSON(self)

	def writeToJSON(self, data, processing_strategy: JSONUtils.WriteJSONStrategy):
		return processing_strategy.writeToJSON(self, data)


	def trackLocation(self, locationdict):
		locationsFromJSON = self.readFromJSON(JSONUtils.TrackedLocationsReadJSONStrategy)
		print("tracking location: "+ locationdict["name"])
		locationsFromJSON[locationdict["pk"]]=locationdict
		#ProfileScraper.writeLocationsToJSON(locationsFromJSON)
		self.writeToJSON(locationsFromJSON, JSONUtils.TrackedLocationsWriteJSONStrategy)


	def isLocationTracked(self, location):
		data = self.readFromJSON(JSONUtils.TrackedLocationsReadJSONStrategy)
		if location.pk in data.keys():
			print("location is already being tracked.")
			return True
		else:
			return False



	def createLocation(self, input, coordinates):
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

	def getMediaLocationCoordinates(self, media):
		coordinates = {'lng': (media.location).lng , 
						'lat': (media.location).lat }
		return coordinates








	def isAlreadyTracked(self, user): #check if database or file already contains this user
		#data = ProfileScraper.getTrackedUsersFromJSON()
		data = self.readFromJSON(JSONUtils.UsersReadJSONStrategy)
		#print(data)
		if user.get('username') in data:
			return True
		else:
			return False


	def trackUser(self, user):
		#username = client.user_info_by_username_v1(username).pk
		username = user.get('username')
		usersfromjson = self.readFromJSON(JSONUtils.UsersReadJSONStrategy)
		print("tracking user: "+ username)
		usersfromjson[username]=user#.dict()
		self.writeToJSON(usersfromjson, JSONUtils.UsersWriteJSONStrategy)






	################

	# EXTEND USERS POOL

	def extendFollowingUsersPoolFromSuggested(self, user, limit):
		try:
			#print("fuck1")
			list = self.instagrapiUtils.getSuggestedUsersFromFBSearch(user)
			#print("fuck2")
		except Exception as e:
			print(e)
			return

		if limit > len(list):
			limit = len(list)

		for usersh in list[0:limit]:
			#print("Fuck come on")
			usertmp = self.instagrapiUtils.convertUserShortToUserv2(usersh)
			username = usertmp.username
			#print("What the fuck")
			usersugg = self.instagrapiUtils.getUserInfoByUsername(username).dict()
			usersugg["LatestPostPartialURL"] = ''
			if self.instagrapiUtils.isProfilePrivate(usersugg) == False:
				if self.isAlreadyTracked(usersugg) == False:
					self.trackUser(usersugg)


	def extendFollowingUsersPoolFromPostTaggedUsers(self,user):
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



	def extendFollowingUsersPoolFromTaggedPostsSection(self, user, limit):
		list = self.instagrapiUtils.getProfileTaggedPosts(user)
		for media in list[0:limit]:
			userposter=self.instagrapiUtils.getUserInfoByUsername(media.user.username).dict()
			user["LatestPostPartialURL"] = ''
			if self.isAlreadyTracked(userposter) == False:
				if self.instagrapiUtils.isProfilePrivate(userposter) == False:
						self.trackUser(userposter)


	def updateUserLatestPostPartialURL(self, user, latestPURL):
		users = self.readFromJSON(JSONUtils.UsersReadJSONStrategy)
		targetuser = users[user.get('username')]
		targetuser["LatestPostPartialURL"] = latestPURL
		users[user.get('username')] = targetuser
		self.writeToJSON(users, JSONUtils.UsersWriteJSONStrategy)

	
	def checkIfPostIsNew(self, indexedPURL, latestPURL):
		if latestPURL == indexedPURL:
			return False
		else:
			return True
		
		
		
	#####################

	# FIND RESTAURANTS

	def crawlRestaurantsFromProfilePosts(self, user, allowExtendUserBase, nPostsAllowed):

		restaurant_tags = ['Restaurant', 'Italian Restaurant','Pub', 'Bar', 'Grocery ', 'Wine', 'Diner', 'Food', 'Meal', 'Breakfast', 'Lunch',
							'Dinner', 'Cafe', 'Tea Room', 'Hotel', 'Pizza', 'Coffee', 'Bakery', 'Dessert', 'Gastropub',
							'Sandwich', 'Ice Cream', 'Steakhouse', 'Pizza place', 'Fast food restaurant', 'Deli']

		postlist = self.instagrapiUtils.getUserPosts(user)
		if nPostsAllowed > len(postlist):
			nPostsAllowed = len(postlist)
		#print(type(user))
		print("here0")
		latestCheckedPURL = self.instagrapiUtils.getLatestPostPartialURLChecked(user)
		for post in postlist[0:nPostsAllowed]:
			print("here1")
			indexedPURL = self.instagrapiUtils.getPostPartialURL(post)
			if self.checkIfPostIsNew(indexedPURL, latestCheckedPURL) == False:  # check if reached a post already checked before
				print("notnew")
				return

			if self.isAlreadyTracked(user):
				self.updateUserLatestPostPartialURL(user, indexedPURL) 
				print("here2")


			if self.instagrapiUtils.hasTaggedLocation(post):
				detailedLocationInfo = self.instagrapiUtils.getDetailedMediaLocationInfo(post)
				print("post location is a: "+str(detailedLocationInfo.category))
				if detailedLocationInfo.category in restaurant_tags and self.isLocationTracked(detailedLocationInfo)==False:
					coordinates = self.getMediaLocationCoordinates(post)
					self.trackLocation(self.createLocation(detailedLocationInfo.dict(), coordinates))

		
		


	def beginScraping(self, allowExtendUserBase, nPostsAllowed):
		
		#print("here0")
		kickoffUser = (self.instagrapiUtils.getUserInfoByUsername("foxybyte.swe")).dict()
		self.trackUser(kickoffUser)
		trackedUsers = self.readFromJSON(JSONUtils.UsersReadJSONStrategy)
		#print("what in the flying fuck");
		if trackedUsers == {}:
			print("here")
			kickoffUser = (self.instagrapiUtils.getUserInfoByUsername("foxybyte.swe"))
			print("here1")
			kickoffUser = kickoffUser
			print("here2")
			self.extendFollowingUsersPoolFromSuggested(kickoffUser, 5)
			trackedUsers = self.readFromJSON(JSONUtils.UsersReadJSONStrategy)
			print("dio se non viene fuori questo lancio il pc dalla finestra")
		
		#print("huhuhuh")
		for user in trackedUsers.values():
			print("MAIN LOOP: " + str(user.get('username')))
			print(user)
			self.crawlRestaurantsFromProfilePosts(user, allowExtendUserBase, 25)
			#if allowExtendUserBase:
				#print("Now extending User  (from main)")
				#self.extendFollowingUsersPoolFromSuggested(user, 5) #follow up to 10 new users. 
				#self.extendFollowingUsersPoolFromTaggedPostsSection(user, nPostsAllowed)  #follows all possible users 
				#self.extendFollowingUsersPoolFromPostTaggedUsers(user) #follows all possible users 

#########################
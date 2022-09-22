import sys, time, os, json
import Levenshtein

from InstagrapiUtils import Media


class LocationProfileFinder:


	@staticmethod
	def getMediaOfLocationUserProfileIfExists(locmedias: list[Media], locname):
		for media in locmedias:
			if LocationProfileFinder.checkForRestaurantUsername(media.user.username, locname) == True:
				return media
		return None

	@staticmethod
	def checkForRestaurantUsername(username, restaurantName: str) -> bool:
		strippedRN = restaurantName.strip()

		if len(strippedRN) > len(username):
			maxL = strippedRN
			minL = username
		else:
			maxL = username
			minL = strippedRN

		distance = Levenshtein.distance(strippedRN, username)
		normalizedL = (len(maxL) - distance)/len(maxL)

		if strippedRN.find(username) != -1 or  normalizedL > 0.5:
			print(username + " and " + strippedRN + " are similar with distance of:" + str(normalizedL))
			return True
		else:
			print("High distance between "+username + " and " + strippedRN + " with score: " + str(normalizedL))
			return False
		

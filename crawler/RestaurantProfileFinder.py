import sys, time, os, json
import Levenshtein


def checkForRestaurantUsername(media, restaurantName):
	#does instagrapi have some name based search method? shall we use Selenium instead?
	# 1. scrape restaurant location
	# 2. compare username of profiles to restaurant location name: need to find a way to find SIMILAR names, not exact matches, which would be uncommon.
	#	this can be done with calculating a likelihood of the name being a possible match. https://stackoverflow.com/questions/10473745/compare-strings-javascript-return-of-likely
	# 3. if found, get profile picture of said account. If not, well... discard the restaurant all together, they have to be on instagram to be on our site.
	strippedRN = restaurantName.strip()
	username = media.user.username

	if len(strippedRN) > len(username):
		maxL = strippedRN
		minL = username
	else:
		maxL = username
		minL = strippedRN

	distance = Levenshtein.distance(strippedRN, username)
	normalizedL = (len(maxL) - distance)/len(maxL)

	if strippedRN.find(username) != -1 or  normalizedL > 0.3:
		print(username + " and " + strippedRN + " are similar with distance of:" + str(normalizedL))
		return True
	else:
		print("High distance between "+username + " and " + strippedRN + " with score: " + str(normalizedL))
		return False
	
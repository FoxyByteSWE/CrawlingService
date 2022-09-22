from ProfileScraper import ProfileScraper
from Crawler import Crawler
from Config import CrawlingServiceConfig
from DBConnection import DBConnection

from location.Location import Location
from location.LocationFactory import LocationFactory
from user.UserProfile import UserProfile
from user.UserProfileFactory import UserProfileFactory
from media.FoxyByteMedia import FoxyByteMedia
from media.FoxyByteMediaFactory import FoxyByteMediaFactory

from user.UserProfile import UserProfile

class CrawlingServiceFacade:

	def __init__(self) -> None:
		self.profileScraper = ProfileScraper()
		self.crawler = Crawler()
		self.crawlingServiceConfig = CrawlingServiceConfig()
		self.db = DBConnection()
		self.db.createServerConnection()
		self.db.createDatabaseConnection("michelinsocial")



	def beginScrapingProfiles(self, allowExtendUserBase: bool, extendUserBasePolicy: int, extendUserBaseLimit: int, nPostsAllowed: int) -> None:
		
		trackedUsers = self.db.readItem("SELECT * FROM users")

		if trackedUsers == []:
			self.profileScraper.findKickoffUsers()
			trackedUsers = self.db.readItem("SELECT * FROM users")

		#Load From JSON Config File.
		places_tags = self.crawlingServiceConfig.locationTags

		for user in trackedUsers:
			userObj = UserProfileFactory.buildFromDB(user)
			self.profileScraper.crawlLocationsFromProfilePosts(userObj, 3, places_tags)

			if allowExtendUserBase == True: # will be fetched from DB during the next crawling session.
				newusers = self.profileScraper.extendUserBaseByPolicy(user, extendUserBaseLimit, self.profileScraper.policies[extendUserBasePolicy])
				for u in newusers:
					self.db.insertItem(u.convertToDict())



	def beginCrawlingLocations(self, nPostsWanted: int) -> None:
		locationsFromQuery = self.db.readItem("SELECT * FROM LOCATIONS")

		for location in locationsFromQuery:
			loc = LocationFactory.buildLocationFromDB(location)
			self.crawler.crawlLocation(loc, nPostsWanted)
			




from ProfileScraper import ProfileScraper
from Crawler import Crawler
from Config import CrawlingServiceConfig
from DBConnection import DBConnection
from location.LocationFactory import LocationFactory
from user.UserProfileFactory import UserProfileFactory
from media.FoxyByteMediaFactory import FoxyByteMediaFactory

from user.UserProfile import UserProfile

class CrawlingServiceFacade:

    def __init__(self) -> None:
        self.profileScraper = ProfileScraper()
        self.crawler = Crawler()
        self.crawlingServiceConfig = CrawlingServiceConfig()
        self.db = DBConnection()
        self.db.createServerConnection()
        self.db.createDatabaseConnection()



    def beginScrapingProfiles(self, allowExtendUserBase: bool, extendUserBasePolicy: int, extendUserBaseLimit: int, nPostsAllowed: int) -> None:
        
        #trackedUsers = self.db.readItem("SELECT * FROM USERS")

        #convert to UserProfile objects

        trackedUsers = [UserProfile(12345,
                                "marcouderzo",
                                False,
                                "12AB34CD")]



        if trackedUsers == []:
            self.profileScraper.findKickoffUsers()
            trackedUsers = self.db.readItem("SELECT * FROM USERS")


        # LOAD FROM DB or JSON
        #places_tags = self.db.readItem("SELECT * FROM PLACES_TAGS")
        places_tags = ['Restaurant', 'Italian Restaurant','Pub', 'Bar', 'Grocery ', 'Wine', 'Diner', 'Food', 'Meal', 'Breakfast', 'Lunch',
                            'Dinner', 'Cafe', 'Tea Room', 'Hotel', 'Pizza', 'Coffee', 'Bakery', 'Dessert', 'Gastropub',
                            'Sandwich', 'Ice Cream', 'Steakhouse', 'Pizza place', 'Fast food restaurant', 'Deli']



        for user in trackedUsers:
            UserProfileFactory.buildFromDatabase(user)
            self.profileScraper.crawlLocationsFromProfilePosts(user, 3, places_tags)

            if allowExtendUserBase == True: # will be fetched from DB during the next crawling session.
                newusers = self.profileScraper.extendUserBaseByPolicy(user, extendUserBaseLimit, self.profileScraper.policies[extendUserBasePolicy])
                for u in newusers:
                    self.db.insertItem(u.convertToDict())



    def beginCrawlingLocations(self, nPostsWanted: int) -> None:
        locationsFromQuery = self.db.readItem("SELECT * FROM LOCATIONS")

        for location in locationsFromQuery:
            loc = LocationFactory.buildLocationFromDB(location)
            self.crawler.crawlLocation(loc, nPostsWanted)
            




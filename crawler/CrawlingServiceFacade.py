from ProfileScraper import ProfileScraper
from Crawler import Crawler
from Config import CrawlingServiceConfig
from DBConnection import DBConnection
from location.LocationFactory import LocationFactory
from user.UserProfileFactory import UserProfileFactory
from media.FoxyByteMediaFactory import FoxyByteMediaFactory

class CrawlingServiceFacade:

    def __init__(self) -> None:
        self.profileScraper = ProfileScraper()
        self.crawler = Crawler()
        self.crawlingServiceConfig = CrawlingServiceConfig()
        self.db = DBConnection()
        self.db.createServerConnection()
        self.db.createDatabaseConnection()



    def beginScrapingProfiles(self, allowExtendUserBase: bool, nPostsAllowed: int) -> None:
        
        trackedUsers = self.db.readItem("SELECT * FROM USERS")


        if trackedUsers == []:
            self.profileScraper.findKickoffUsers()

        # LOAD FROM DB or JSON
        places_tags = self.db.readItem("SELECT * FROM PLACES_TAGS")
        places_tags = ['Restaurant', 'Italian Restaurant','Pub', 'Bar', 'Grocery ', 'Wine', 'Diner', 'Food', 'Meal', 'Breakfast', 'Lunch',
                            'Dinner', 'Cafe', 'Tea Room', 'Hotel', 'Pizza', 'Coffee', 'Bakery', 'Dessert', 'Gastropub',
                            'Sandwich', 'Ice Cream', 'Steakhouse', 'Pizza place', 'Fast food restaurant', 'Deli']

        for user in trackedUsers: #.values():
            UserProfileFactory.buildFromDatabase(user) # TODO: pass parameters
            self.profileScraper.crawlLocationsFromProfilePosts(user, 3, places_tags)


    def beginCrawlingLocations(self, nPostsWanted: int) -> None:
        locationsFromQuery = self.db.readItem("SELECT * FROM LOCATIONS") # either pass a query as string or make it a strategy pattern.

        for location in locationsFromQuery: # list of dicts?
            loc = LocationFactory.buildLocationFromDB(location)
            self.crawler.crawlLocation(loc, 2)
            




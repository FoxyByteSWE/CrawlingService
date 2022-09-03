from ProfileScraper import ProfileScraper
from Crawler import Crawler
from Config import CrawlingServiceConfig

class CrawlingServiceFacade:

    def __init__(self) -> None:
        self.profileScraper = ProfileScraper()
        self.crawler = Crawler()
        self.crawlingServiceConfig = CrawlingServiceConfig()
        #self.db = DBConnection()

    

    def beginCrawlingLocations(self, nPostsWanted: int) -> None:
        locationsDict = DBConnection.readFromDB() #db
        self.crawlAllLocations(locationsDict, 2)


    def beginScrapingProfiles(self, allowExtendUserBase: bool, nPostsAllowed: int) -> None:
        
        trackedUsers = DBConnection.readFromDB() #and create users of our type
        if trackedUsers == []:
            self.crawler.createKickoffUser()

        # LOAD FROM DB
        #places_tags = readFromDB()
        places_tags = ['Restaurant', 'Italian Restaurant','Pub', 'Bar', 'Grocery ', 'Wine', 'Diner', 'Food', 'Meal', 'Breakfast', 'Lunch',
                            'Dinner', 'Cafe', 'Tea Room', 'Hotel', 'Pizza', 'Coffee', 'Bakery', 'Dessert', 'Gastropub',
                            'Sandwich', 'Ice Cream', 'Steakhouse', 'Pizza place', 'Fast food restaurant', 'Deli']

        for user in trackedUsers.values():
            self.profileScraper.crawlPlacesFromProfilePosts(user, 3)

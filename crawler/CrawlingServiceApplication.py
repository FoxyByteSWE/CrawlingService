from  UserProfileRestaurantScraper import ProfileScraper
#from Crawler import Crawler
from Config import CrawlingServiceConfig



def main(): 
    config = CrawlingServiceConfig()

    #crawler = Crawler()
    userProfileRestaurantScraper = ProfileScraper()
    
    #print("Starting Crawling Process...")

    #crawler.beginCrawling(config.nPostsWantedForEachLocation)

    #input("Press Any Key To Begin Scraping The Locations...")

    userProfileRestaurantScraper.beginScraping(config.allowExtendUserBase,
                                               config.nPostsAllowedForProfileScraping)






if __name__ == "__main__":
	main()




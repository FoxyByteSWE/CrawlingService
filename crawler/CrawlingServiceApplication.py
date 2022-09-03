from CrawlingServiceFacade import CrawlingServiceFacade



def main(): 
    crawlingService = CrawlingServiceFacade()
    
    crawlingService.beginScrapingProfiles(True, 3)

    crawlingService.beginCrawlingLocations(3)





if __name__ == "__main__":
	main()




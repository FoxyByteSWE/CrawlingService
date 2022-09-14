from CrawlingServiceFacade import CrawlingServiceFacade



def main(): 
    crawlingService = CrawlingServiceFacade()
    
    crawlingService.beginScrapingProfiles(crawlingService.crawlingServiceConfig.allowExtendUserBase, 
                                        crawlingService.crawlingServiceConfig.extendUserBasePolicyNumber, 
                                        crawlingService.crawlingServiceConfig.nMaxUsersToAdd,
                                        crawlingService.crawlingServiceConfig.nPostsAllowedForProfileScraping)

    crawlingService.beginCrawlingLocations(crawlingService.crawlingServiceConfig.nPostsWantedForEachLocation)





if __name__ == "__main__":
	main()




from CrawlingServiceFacade import CrawlingServiceFacade



def main(): 
    crawlingService = CrawlingServiceFacade()
    
    crawlingService.beginScrapingProfiles(crawlingService.crawlingServiceConfig.allowExtendUserBase, 
                                        crawlingService.crawlingServiceConfig.extendUserBasePolicyNumber, 
                                        crawlingService.crawlingServiceConfig.nMaxUsersToAdd,
                                        crawlingService.crawlingServiceConfig.nPostsWantedForEachLocation)

    #crawlingService.beginCrawlingLocations(3)





if __name__ == "__main__":
	main()




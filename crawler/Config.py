from JSONUtils import JSONUtils

class CrawlingServiceConfig:


    allowExtendUserBase = True   
    nPostsAllowedForProfileScraping = 40
    nPostsWantedForEachLocation = 50

    def readFromJSON(self, processing_strategy: JSONUtils.ReadJSONStrategy):
        return processing_strategy.readFromJSON(self)


    def __init__(self):
        config = self.readFromJSON(JSONUtils.ConfigReadJSONStrategy)
        
        self.sleepTime = config["sleepTime"]
        self.allowExtendUserBase = True if config["allowExtendUserBase"] == "True" else False
        self.extendUserBasePolicy = config["extendUserBasePolicy"]
        self.nMaxUsersToAdd = config["nMaxUsersToAdd"]
        self.nPostsAllowedForProfileScraping = config["nPostsAllowedForProfileScraping"]
        self.nPostsWantedForEachLocation = config["nPostsWantedForEachLocation"]

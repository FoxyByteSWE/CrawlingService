from JSONUtils import JSONUtils

class CrawlingServiceConfig:
    

    allowExtendUserBase = True   
    nPostsAllowedForProfileScraping = 40
    nPostsWantedForEachLocation = 50

    def readFromJSON(processing_strategy: JSONUtils.ReadJSONStrategy):
        return processing_strategy.readFromJSON()


    def __init__(self):
        config = self.readFromJSON(JSONUtils.ConfigReadJSONStrategy())
        

        self.allowExtendUserBase = True if config["allowExtendUserBase"] == "True" else False
        self.nPostsAllowedForProfileScraping = config["nPostsAllowedForProfileScraping"]
        self.nPostsWantedForEachLocation = config["nPostsWantedForEachLocation"]
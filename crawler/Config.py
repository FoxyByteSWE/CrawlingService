import sys, json


class CrawlingServiceConfig:

    def readFromJSON(self):
        filepath = (str(sys.path[0]))+"/data/config.json"
        with open(filepath) as usersFile:
            try:
                data = json.load(usersFile)
                return data
            except Exception as e:
                print(e)
                return {}


    def __init__(self):
        config = self.readFromJSON()
    
        self.allowExtendUserBase = True if config["allowExtendUserBase"] == "True" else False
        self.extendUserBasePolicyNumber = config["extendUserBasePolicyNumber"]
        self.extendUserBasePolicy = config["extendUserBasePolicy"]
        self.nMaxUsersToAdd = config["nMaxUsersToAdd"]
        self.nPostsAllowedForProfileScraping = config["nPostsAllowedForProfileScraping"]
        self.nPostsWantedForEachLocation = config["nPostsWantedForEachLocation"]

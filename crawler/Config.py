import sys, json

class CrawlingServiceConfigBase(type): #SINGLETON

    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]



class CrawlingServiceConfig(metaclass=CrawlingServiceConfigBase):

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
        self.instagramUsername = config["instagramUsername"]
        self.instagramPassword = config["instagramPassword"]
        self.locationTags = config["locationTags"]
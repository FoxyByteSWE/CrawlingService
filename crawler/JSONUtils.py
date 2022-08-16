
from abc import ABC, abstractmethod
import os, json, sys, time



class JSONUtils:
    ##################### WRITING TO JSON ##########################



    class WriteJSONStrategy(ABC):
        @abstractmethod
        def writeToJSON(self, data):
            pass



    class UsersWriteJSONStrategy(WriteJSONStrategy):
        def writeToJSON(self, data): #writenewuserstojsonfile
            jsondump= json.dumps(data)
            with open((str(sys.path[0]))+"/data/trackedUsers.json", "w") as outfile:
                outfile.write(jsondump)	

    class TrackedLocationsWriteJSONStrategy(WriteJSONStrategy):
        def writeToJSON(self, data): #writenewuserstojsonfile
            jsondump= json.dumps(data)
            with open((str(sys.path[0]))+"/data/locations.json", "w") as outfile:
                outfile.write(jsondump)

    class CrawledDataWriteJSONStrategy(WriteJSONStrategy):
        def writeToJSON(self, data):
            jsondump= json.dumps(data)
            with open((str(sys.path[0]))+"/data/locationsData.json", "w") as outfile:
                outfile.write(jsondump)

                


    class InitParenthesisWriteJSONStrategy(WriteJSONStrategy):
        def writeToJSON(self, data = "{}"):
            with open((str(sys.path[0]))+"/data/trackedUsers.json", "w") as outfile:
                outfile.write(data)	






    ######################### READING FROM JSON #####################



    class ReadJSONStrategy(ABC):
        @abstractmethod
        def readFromJSON(self):
            pass





    class TrackedLocationsReadJSONStrategy(ReadJSONStrategy):
        def readFromJSON(self):
            filepath = (str(sys.path[0]))+"/data/locations.json"
            with open(filepath) as locationsFile:
                try:
                    data = json.load(locationsFile)
                    return data
                except Exception as e:
                    print(e)
                    return {}

    class UsersReadJSONStrategy(ReadJSONStrategy):
        def readFromJSON(self):
            filepath = (str(sys.path[0]))+"/data/trackedUsers.json"
            with open(filepath) as usersFile:
                try:
                    data = json.load(usersFile)
                    return data
                except Exception as e:
                    print(e)
                    return {}

    class CrawledDataReadJSONStrategy(ReadJSONStrategy):
        def readFromJSON(self):
            filepath = (str(sys.path[0]))+"/data/locationsData.json"
            with open(filepath) as locationsFile:
                try:
                    data = json.load(locationsFile)
                    return data
                except Exception as e:
                    print(e)
                    return {}

    
    class ConfigReadJSONStrategy(ReadJSONStrategy):
        def readFromJSON(self):
            filepath = (str(sys.path[0]))+"/data/config.json"
            with open(filepath) as usersFile:
                try:
                    data = json.load(usersFile)
                    return data
                except Exception as e:
                    print(e)
                    return {}

            
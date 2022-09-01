import os, json, sys, time
from re import M
from instagrapi import Client
import instagrapi
from typing import Dict
import pprint

from instagrapi.types import Media
from instagrapi.types import Location
from instagrapi.types import User

class InstagrapiUtilsBase(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]



class InstagrapiUtils(metaclass=InstagrapiUtilsBase):

    client = None

    def __init__(self) -> None:
        self.createLoggedInClient()



    def createLoggedInClient(self) -> None:
        try:
            self.client = Client(self.loadCookies())
            self.client.login("foxybyte.swe", "tipregofunzionaswe")
            print("Client Logged-In to Instagrapi")
        except Exception as e:
            print("Something went wrong during Instagrapi Login: " + str(e))
            exit()


    def save_cookies(self) -> None:
        """
        Save the cookies of the client in a local json file called cookie.json.
        """
        json.dump(self.client.get_settings(), open((str(sys.path[0]))+"/data/cookie.json", 'w'))

    def loadCookies(self):
        return json.loads(open((str(sys.path[0]))+"/data/cookie.json").read())




    def getLocationPkCodeFromName(self, locationName: str) -> int:
        locList = (self.client.fbsearch_places(locationName)[0])
        pkCode = locList.pk
        return pkCode

    def getMostRecentMediasFromLocation(self, locationName: str) -> list:
        pkCode = self.getLocationPkCodeFromName(locationName)
        mediaListFromLocation = self.client.location_medias_recent(pkCode)
        return mediaListFromLocation


    def getMediaLocationCoordinates(self, media) -> dict:
        coordinates = {'lng': ((media.location).lng) , 
                       'lat': ((media.location).lat) }
        return coordinates


    def getMediaURL(self, media: Media):  #TODO: test for a multi-media (album) post
        #print("here")
        if media.media_type==1:
            return media.thumbnail_url
        if media.media_type==2:
            return media.video_url
        if media.media_type==8: #album
            album = media.resources
            list=[]
            for item in album:
                if media.media_type == 1:
                    list.append(item.thumbnail_url)
                elif media.media_type == 2:
                    list.append(item.video_url)
            return list


    def parseTakenAtTime(self, input) -> list:
        time = []
        time.append(input.year)
        time.append(input.month)
        time.append(input.day)
        time.append(input.hour)
        time.append(input.minute)
        time.append(input.second)
        return time

    def parseTakenAtLocation(self, media) -> dict:
        input = self.getDetailedMediaLocationInfo(media)
        coordinates = self.getMediaLocationCoordinates(media)
        dict = {}
        dict["pk"] = input["pk"]
        dict["name"] = input["name"]
        dict["address"] = input["address"]
        dict["coordinates"] = [coordinates["lng"], coordinates["lat"]]
        dict["category"] = input["category"]
        dict["phone"] = input["phone"]
        dict["website"] = input["website"]
        return dict;

    def parseMediaUrl(self, input: list) -> str:
        url = str(input)
        start = url.find("'") + 1
        url = url[start:]
        end = url.find("'")
        url = url[:end]
        return url;




    def getDetailedMediaLocationInfo(self, media: Media) -> Location: 
        mediainfo = self.client.media_info_v1(media.pk)
        if mediainfo.location != None:
            return self.client.location_info((mediainfo.location).pk)
        else:
            return None

    def getUserPosts(self, user, amount) -> list[Media]:
        userpk = user.pk
        return self.client.user_medias_v1(userpk, amount)

    def getSuggestedUsersFromFBSearch(self, user: User):
        print("WARNING: CHECK InstagrapiUtils.getSuggestedUsersFromFBSearch(user)")
        pk = user.pk
        res =  self.client.fbsearch_suggested_profiles(pk)  # For some reason an exception is thrown: Not eligible for chaining. 
        return res

    def hasTaggedLocation(self, media: Media) -> bool:
        return media.location != None

    def getUserIDofTagged(self, user: User) -> list[Media]: 
        #time.sleep(2)
        userpk = user.pk
        return self.client.usertag_medias(userpk)

    def getProfileTaggedPosts(self, user: User) -> list[Media]:
        userpk = user.pk
        return self.client.usertag_medias(userpk)


    ###########################################

    # USER CONVERTERS

 #   def convertUsertagToUser(self, usertag):
 #       return usertag.user

    def convertUserShortToUserv2(self, usershort):
        #print("convertUserShortToUserv2")
        return self.client.user_info_by_username_v1(usershort['username'])

    ########################################

    # LOCATION GETTERS
#
#    def getLocationFromPost(self, media: dict):
#        return media.get('location')
#
#    def getLocationPkCode(self, location: dict) -> int:
#        return location.get('pk')
#
#    def hasTaggedLocation(self, post: dict) -> bool:
#        return post.get('location') != None 

import os, json, sys, datetime
from re import M
from instagrapi import Client
import instagrapi
from typing import Dict
import pprint

from instagrapi.types import Media
from instagrapi.types import Location
from instagrapi.types import User
from instagrapi.types import UserShort

from Config import CrawlingServiceConfig

class InstagrapiUtilsBase(type): #SINGLETON

    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]



class InstagrapiUtils(metaclass=InstagrapiUtilsBase):

    client = None

    def __init__(self) -> None:
        value = self.createLoggedInClient()



    def createLoggedInClient(self) -> None:
        try:
            self.client = Client(self.loadCookies())
            config = CrawlingServiceConfig()
            self.client.login(config.instagramUsername, config.instagramPassword)
            print("Client Logged-In to Instagrapi")
        except Exception as e:
            print("Something went wrong during Instagrapi Login: " + str(e))
            return -1

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

    def getMostRecentMediasFromLocation(self, locationName: str, amount: int) -> list[Media]:
        pkCode = self.getLocationPkCodeFromName(locationName)
        mediaListFromLocation = self.client.location_medias_recent(pkCode, amount)
        return mediaListFromLocation

    def getMediaLocationCoordinates(self, media: Media) -> dict:
        coordinates = {'lng': ((media.location).lng) , 
                       'lat': ((media.location).lat) }
        return coordinates

    def getMediaURL(self, media: Media):  #TODO: test for a multi-media (album) post
        #print("here")
        if media.media_type==1:
            return [media.thumbnail_url]
        if media.media_type==2:
            return [media.video_url]
        if media.media_type==8: #album
            album = media.resources
            list=[]
            for item in album:
                if item.media_type == 1:
                    list.append(item.thumbnail_url)
                elif item.media_type == 2:
                    list.append(item.video_url)
            return list

    def parseTakenAtTime(self, input: datetime) -> list:
        time = []
        time.append(input.year)
        time.append(input.month)
        time.append(input.day)
        time.append(input.hour)
        time.append(input.minute)
        time.append(input.second)
        return time

    def parseTakenAtLocation(self, media: Media) -> dict: #SUBSCRIPTING TO .attr
        input = self.getDetailedMediaLocationInfo(media)
        coordinates = self.getMediaLocationCoordinates(media)
        dict = {}
        dict["pk"] = input.pk
        dict["name"] = input.name
        dict["address"] = input.address
        dict["coordinates"] = [coordinates["lng"], coordinates["lat"]]
        dict["category"] = input.category
        dict["phone"] = input.phone
        dict["website"] = input.website
        return dict;

    def parseMediaUrl(self, inputlist: list) -> list[str]:
        newlist = []
        for item in inputlist:
            url = str(item)
            start = url.find("'") + 1
            url = url[start:]
            newlist.append(url)
        print(newlist)
        return newlist

    def getDetailedMediaLocationInfo(self, media: Media) -> Location: 
        mediainfo = self.client.media_info_v1(media.pk)
        if mediainfo.location != None:
            return self.client.location_info((mediainfo.location).pk)
        else:
            return None

    def getUserPosts(self, userpk: int, amount) -> list[Media]:
        return self.client.user_medias_v1(userpk, amount)

    def getSuggestedUsersFromFBSearch(self, userpk: int) -> list[UserShort]: #following link -> URL signature expired
        print("WARNING: CHECK InstagrapiUtils.getSuggestedUsersFromFBSearch")
        res =  self.client.fbsearch_suggested_profiles(userpk)  # For some reason an exception is thrown: Not eligible for chaining. 
        return res

    def hasTaggedLocation(self, media: Media) -> bool:
        return media.location != None

    def getProfileTaggedPosts(self, userpk: int) -> list[Media]:
        return self.client.usertag_medias(userpk)

    def getPostTaggedPeople(self, post: Media):
        return post.usertags

    def isProfilePrivate(self, user: User) -> bool:
        return user.is_private

    def getUserInfoByUsername(self, username: str) -> User:
        return self.client.user_info_by_username_v1(username)

    def convertUserShortToUserv2(self, usershort: UserShort):
        return self.client.user_info_by_username_v1(usershort['username'])
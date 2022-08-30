import os, json, sys, time
from re import M
from instagrapi import Client
import instagrapi
from typing import Dict
import pprint

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
        locList = (self.client.fbsearch_places(locationName)[0]).dict()
        pkCode = locList.get('pk')
        return pkCode

    def getTopMediasFromLocation(self, locationName: str) -> list:
        print(locationName)
        pkCode = self.getLocationPkCodeFromName(locationName)
        mediaListFromLocation = self.client.location_medias_top(pkCode)
        return mediaListFromLocation

    def getMostRecentMediasFromLocation(self, locationName: str) -> list:
        pkCode = self.getLocationPkCodeFromName(locationName)
        mediaListFromLocation = self.client.location_medias_recent(pkCode)
        return mediaListFromLocation

    def getPostPartialURL(self, media: dict) -> str:
        return media.get('code')


    def getLatestPostPartialURLChecked(self, user: dict) -> str:
        return user.get("LatestPostPartialURL")

    def getMediaType(self, media) -> int:
        return media.get('media_type')

    def getCaptionText(self, media) -> str:
        return media.get('caption_text')

    def getMediaTime(self, media):
        return media.get('taken_at')

    def getMediaLocationCoordinates(self, media: dict) -> dict:
        coordinates = {'lng': (media.get('location').get('lng')) , 
                       'lat': (media.get('location').get('lat')) }
        return coordinates


    def getMediaLocationPK(self, media: dict)-> int:
            return media.get('pk')

    def getMediaLikeCount(self, media:dict) -> int:
        return media.get('like_count')

    def getMediaURL(self, media: dict):  #TODO: test for a multi-media (album) post
        #print("here")
        if self.getMediaType(media)==1:
            return media.get('thumbnail_url')
        if self.getMediaType(media)==2:
            return media.get('video_url')
        if self.getMediaType(media)==8: #album
            album = media.get('resources')
            list=[]
            for item in album:
                if self.getMediaType(item) == 1:
                    list.append(item.get('thumbnail_url'))
                elif self.getMediaType(item) == 2:
                    list.append(item.get('video_url'))
            return list



    def getDetailedMediaLocationInfo(self, media:dict) -> dict: 
        mediainfo = self.client.media_info_v1(media.get('pk'))
        if mediainfo.location != None:
            return self.client.location_info((mediainfo.location).pk).dict()
        else:
            return None


    def getUsernameFromID(self, userid) -> str:
        #print("getUsernameFromID")
        #time.sleep(2)
        return self.client.username_from_user_id(userid)

    def getUserIDfromUsername(self, username):
        return self.getUserInfoByUsername(username).pk

    def getUserInfoByUsername(self, username: str) -> dict:
        #print("getUserInfoByUsername")
        #time.sleep(2)
        return self.client.user_info_by_username_v1(username)

    def getUserPosts(self, user: dict) -> list:
        #time.sleep(2)
        userpk = user.get('pk')
        return self.client.user_medias_v1(userpk)

    def getSuggestedUsersFromFBSearch(self, user):
        print("WARNING: CHECK InstagrapiUtils.getSuggestedUsersFromFBSearch(user)")
        pk = user.get('pk')
        res =  self.client.fbsearch_suggested_profiles(pk)  # For some reason an exception is thrown: Not eligible for chaining. 
        return res

    def isProfilePrivate(self, user: dict) -> bool:
        return user.get('is_private')

    def getPostTaggedPeople(self, post: dict) -> list:
        return post.usertags

    def getUserIDofTagged(self, user: dict) -> list: 
        #time.sleep(2)
        userpk = user.get('pk')
        return self.client.usertag_medias(userpk)

    def getProfileTaggedPosts(self, user: dict) -> list:
        userpk = user.get('pk')
        return self.client.usertag_medias(userpk)


    ###########################################

    # USER CONVERTERS

    def convertUsertagToUser(self, usertag):
        return usertag.user

    def convertUserShortToUser(self, usershort):
        #print("convertUserShortToUser")
        return self.client.user_info_by_username(usershort.username)

    def convertUserShortToUserv2(self, usershort):
        #print("convertUserShortToUserv2")
        return self.client.user_info_by_username_v1(usershort['username'])

    ########################################

    # LOCATION GETTERS

    def getLocationFromPost(self, media: dict):
        return media.get('location')

    def getLocationPkCode(self, location):
        return location.get('pk')

    def hasTaggedLocation(self, post: dict) -> bool:
        return post.get('location') != None 

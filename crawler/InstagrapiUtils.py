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
        ret = self.createLoggedInClient()



    def createLoggedInClient(self):
        try:
            self.client = Client()
            self.client.login("foxybyte.swe", "tipregofunzionaswe")
            print("Client Logged-In to Instagrapi")
        except Exception as e:
            print("Something went wrong: " + str(e))
            exit()
        #client.dump_settings((str(sys.path[0]))+"/data/settingsdump.json")
        #self.client.load_settings((str(sys.path[0]))+"/data/settingsdump.json")



    def getLocationPkCodeFromName(self, locationName):
        locList = (self.client.fbsearch_places(locationName)[0]).dict()
        pkCode = locList.get('pk')
        return pkCode

    def getTopMediasFromLocation(self, locationName):
        print(locationName)
        pkCode = self.getLocationPkCodeFromName(locationName)
        mediaListFromLocation = self.client.location_medias_top(pkCode)
        return mediaListFromLocation

    def getMostRecentMediasFromLocation(self, locationName):
        pkCode = self.getLocationPkCodeFromName(locationName)
        mediaListFromLocation = self.client.location_medias_recent(pkCode)
        return mediaListFromLocation

    def getPostPartialURL(self, media):
        #print("media is:")
        #print(media)
        return media.code


    def getLatestPostPartialURL(self, user):
        print(type(user))
        medias = self.getUserPosts(user)
        #print("medias[0] is: ")
        #print(medias[0])
        return self.getPostPartialURL(medias[0])

    def getMediaType(self, media):
        return media.media_type

    def getCaptionText(self, media):
        return media.caption_text

    def getMediaTime(self, media):
        return media.taken_at

    def getMediaLocationCoordinates(self, media):
        coordinates = {'lng': (media.location).lng , 
                    'lat': (media.location).lat }
        return coordinates


    def getMediaLocationPK(self, media):
            return media.pk

    def getMediaLikeCount(self, media):
        return media.like_count

    def getMediaURL(self, media):
        #print("here")
        if self.getMediaType(media)==1:
            return media.thumbnail_url
        if self.getMediaType(media)==2:
            return media.video_url
        if self.getMediaType(media)==8: #album
            album = media.resources
            list=[]
            for item in album:
                if self.getMediaType(item) == 1:
                    list.append(item.thumbnail_url)
                elif self.getMediaType(item) == 2:
                    list.append(item.video_url)
            return list



    def getDetailedMediaLocationInfo(self, media):  # this works and retrieves all category and other data
        mediainfo = self.client.media_info_v1(media.pk)
        if mediainfo.location != None:
            return self.client.location_info((mediainfo.location).pk)
        else:
            return None


    def getUsernameFromID(self, userid):
        #print("getUsernameFromID")
        #time.sleep(2)
        return self.client.username_from_user_id(userid)

    def getUserIDfromUsername(self, username):
        #print("getUserIDfromUsername")
        return self.getUserInfoByUsername(username).pk
        #return client.user_id_from_username(username)

    def getUserInfoByUsername(self, username):
        #print("getUserInfoByUsername")
        #time.sleep(2)
        return self.client.user_info_by_username_v1(username)

    def getUserPosts(self, user):
        #time.sleep(2)
        if type(user) is dict:
            userpk = user.get('pk')
        else:
            userpk = user.pk
        return self.client.user_medias_v1(userpk)

    def getSuggestedUsersFromFBSearch(self, user):
        #time.sleep(2)
        #userpk = user.get('pk')
        #userpk = user['pk'];
        #print(user.pk)
        if type(user) is dict:
            return self.client.fbsearch_suggested_profiles(user.get('pk'))
        else:
            return self.client.fbsearch_suggested_profiles(user.pk)

    def isProfilePrivate(self, user):
        return user.get('is_private')

    def getPostTaggedPeople(self, post):
        return post.usertags

    def getUserIDofTagged(self, user):
        #time.sleep(2)
        userpk = user.get('pk')
        return self.client.usertag_medias(userpk)

    def getProfileTaggedPosts(self, user):
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

    def getLocationFromPost(self, media):
        return media.location

    def getLocationPkCode(self, location):
        return location.pk

    def hasTaggedLocation(self, post):
        return post.location != None   # TODO: Da Testare per il != None

import os, json, sys, time
from instagrapi import Client
import instagrapi
from typing import Dict
import pprint

    
    
class InstagrapiUtils:

    def createLoggedInClient():
        client = Client()
        client.login("foxybyte.swe", "Swe_2022")
        #client.dump_settings((str(sys.path[0]))+"/data/settingsdump.json")
        #client.load_settings((str(sys.path[0]))+"/data/settingsdump.json")
        return client

    def getLocationPkCodeFromName(locationName, client):
        locList = (client.fbsearch_places(locationName)[0]).dict()
        pkCode = locList.get("pk")
        return pkCode

    def getTopMediasFromLocation(locationName, client):
        pkCode = InstagrapiUtils.getLocationPkCodeFromName(locationName, client)
        mediaListFromLocation = client.location_medias_top(pkCode)
        return mediaListFromLocation

    def getMostRecentMediasFromLocation(locationName, client):
        pkCode = InstagrapiUtils.getLocationPkCodeFromName(locationName, client)
        mediaListFromLocation = client.location_medias_recent(pkCode)
        return mediaListFromLocation

    def getMediaType(media):
        return media.media_type

    def getCaptionText(media):
        return media.caption_text

    def getMediaTime(media):
        return media.taken_at

    def getMediaLocationCoordinates(media):
        coordinates = {'lng': (media.location).lng , 
                    'lat': (media.location).lat }
        return coordinates


    def getMediaLocationPK(media):
            return media.pk

    def getMediaLikeCount(media):
        return media.like_count

    def getMediaURL(media):
        if InstagrapiUtils.getMediaType(media)==1:
            return media.thumbnail_url
        if InstagrapiUtils.getMediaType(media)==2:
            return media.video_url
        if InstagrapiUtils.getMediaType(media)==8: #album
            album = media.resources
            list=[]
            for item in album:
                if InstagrapiUtils.getMediaType(item) == 1:
                    list.append(item.thumbnail_url)
                elif InstagrapiUtils.getMediaType(item) == 2:
                    list.append(item.video_url)
            return list

    def getPostPartialURL(media):
        return media.code


    def getDetailedMediaLocationInfo(media, client):  # this works and retrieves all category and other data
        mediainfo = client.media_info_v1(media.pk)
        if mediainfo.location != None:
            return client.location_info((mediainfo.location).pk)
        else:
            return None


    def getUsernameFromID(userid, client):
        #print("getUsernameFromID")
        #time.sleep(2)
        return client.username_from_user_id(userid)

    def getUserIDfromUsername(username, client):
        #print("getUserIDfromUsername")
        return InstagrapiUtils.getUserInfoByUsername(username, client).pk
        #return client.user_id_from_username(username)

    def getUserInfoByUsername(username, client):
        #print("getUserInfoByUsername")
        #time.sleep(2)
        return client.user_info_by_username_v1(username)

    def getUserPosts(userid, client):
        #time.sleep(2)
        return client.user_medias_v1(userid)

    def getSuggestedUsersFromFBSearch(userid, client):
        #time.sleep(2)
        return client.fbsearch_suggested_profiles(userid)

    def isProfilePrivate(user):
        return user.is_private

    def getPostTaggedPeople(post):
        return post.usertags

    def getUserIDofTagged(userid, client):
        #time.sleep(2)
        return client.usertag_medias(userid)

    def getProfileTaggedPosts(userid, client):
        #time.sleep(2)
        return client.usertag_medias(userid)


    ###########################################

    # USER CONVERTERS

    def convertUsertagToUser(usertag):
        return usertag.user

    def convertUserShortToUser(usershort,client):
        #print("convertUserShortToUser")
        return client.user_info_by_username(usershort.username)

    def convertUserShortToUserv2(usershort,client):
        #print("convertUserShortToUserv2")
        return client.user_info_by_username_v1(usershort["username"])

    ########################################

    # LOCATION GETTERS

    def getLocationFromPost(media):
        return media.location

    def getLocationPkCode(location):
        return location.pk

    def hasTaggedLocation(post):
        return post.location != None   # TODO: Da Testare per il != None

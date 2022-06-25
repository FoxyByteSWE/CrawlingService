import os, json, sys
from instagrapi import Client
import instagrapi
from typing import Dict




def createLoggedInClient():
    client = Client()
    client.login("foxybyte.swe", "Swe_2022")
    #client.dump_settings(str(sys.path[0])+"/data/settingsdump.json")
    client.load_settings(str(sys.path[0])+"/data/settingsdump.json")
    return client

def followUser(userid, client):
    print("dummy following user: "+ (client.user_info(userid)).username)
    #return client.user_follow(userid)

def getUsernameFromID(userid, client):
    return client.username_from_user_id(userid)

def getUserIDfromUsername(username, client):
    return client.user_id_from_username(username)

def getUserFollowing(userid, client):
    return client.user_following(userid)

def enablePostNotifications(userid, client): #scrape profile if new posts are posted.
    return client.enable_posts_notifications(userid)

def getUserPosts(userid, client):
    return client.user_medias_v1(userid)

def getLocationFromPost(media):
    return media.location

def getLocationPkCode(location):
    return location.pk

def classifyLocationType(location):  #reimplement with new location tags
    if location.category == "Restaurant":
        return 1
    else:
        return -1

def hasTaggedLocation(post):
    return post.location != None

def getProfileTaggedPosts(userid, client):
    return client.usertag_medias(userid)


def getPostTaggedPeople(post):
    return post.usertags

def convertUsertagToUser(usertag):
    return usertag.user

def getUserIDofTagged(userid, client):
    return client.usertag_medias(userid)

def getPostPKCode(post, client):
    return post.pk

def getDetailedMediaLocationInfo(post, client):  # this works and retrieves all category and other data
    mediainfo = client.media_info_v1(post.pk)
    if mediainfo.location != None:
        return client.location_info((mediainfo.location).pk)
    else:
        return None

def getSuggestedUsersFromFBSearch(userid, client):
    return client.fbsearch_suggested_profiles(userid)


def convertUserShortToUser(usershort,client):
    return client.user_info_by_username(usershort.username)

def isProfilePrivate(user):
    return user.is_private


################

# EXTEND USERS POOL

def extendFollowingUsersPoolFromSuggested(userid, client):
    list = getSuggestedUsersFromFBSearch(userid, client)
    for usersh in list:
        user = convertUserShortToUser(usersh, client)
        if isProfilePrivate(user) == False:
            followUser(user.pk)

def extendFollowingUsersPoolFromPostTaggedUsers(post,client):
    list = getPostTaggedPeople(post)
    for usertag in list:
        usersh=convertUsertagToUser(usertag)
        user = convertUserShortToUser(usersh, client)
        if isProfilePrivate(user) == False:
            followUser(user.pk)


def extendFollowingUsersPoolFromTaggedPostsSection(userid, client):
    list = getProfileTaggedPosts(userid, client)
    for media in list:
        user=media.user
        if isProfilePrivate(user) == False:
            followUser(user.pk)


def extendUsersFollowingPool(post, userid, client):
    extendFollowingUsersPoolFromPostTaggedUsers(post)
    extendFollowingUsersPoolFromTaggedPostsSection(userid)
    extendFollowingUsersPoolFromSuggested(userid)
    



        

def writeCrawledDataToJson(locationsData): 
	jsondump= json.dumps(locationsData)
	with open((str(sys.path[0]))+"/data/locations.json", "a") as outfile:
		outfile.write(jsondump)


#####################

# FIND RESTAURANTS

def crawlRestaurantsFromProfilePosts(userid, client):

    restaurant_tags = ['Restaurant', 'Pub', 'Bar', 'Grocery ', 'Wine', 'Diner', 'Food', 'Meal', 'Breakfast', 'Lunch',
                           'Dinner', 'Cafe', 'Tea Room', 'Hotel', 'Pizza', 'Coffee', 'Bakery', 'Dessert', 'Gastropub',
                           'Sandwich', 'Ice Cream', 'Steakhouse']

    postlist = getUserPosts(userid, client)
    newrestaurants = []
    for post in postlist:
        if getPostTaggedPeople(post) != None:
            extendFollowingUsersPoolFromPostTaggedUsers(post)

        if hasTaggedLocation(post):
            detailedLocationInfo = getDetailedMediaLocationInfo(post, client)
            print(detailedLocationInfo.category)
            if detailedLocationInfo.category in restaurant_tags:
                newrestaurants.append(detailedLocationInfo.dict())

    #print(newrestaurants)
    writeCrawledDataToJson(newrestaurants)
    return newrestaurants


#########################



#################################################################

def main():
    client = createLoggedInClient()
    #followedUsers = getUserFollowing(getUserIDfromUsername("foxybyte.swe", client), client)
    usertest = getUserIDfromUsername("alsaiso", client)
    crawlRestaurantsFromProfilePosts(usertest, client)



################################################################

if __name__ == "__main__":
    main()

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

def trackUser(user, client,newusers):
    username=(client.user_info(user.pk)).username
    print("tracking user: "+ username)
    newusers[username]=user.dict()
    return newusers

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


def getUserInfoByUsername(username, client):
    return client.user_info_by_username(username)

def convertUserShortToUserv2(usershort,client):
    return client.user_info_by_username(usershort["username"])

def isProfilePrivate(user):
    return user.is_private


def writeNewUsersToJSONFile(newusers):
    jsondump= json.dumps(newusers)
    with open((str(sys.path[0]))+"/data/trackedUsers.json", "a") as outfile:
	    outfile.write(jsondump)

def isAlreadyTracked(user): #check if database or file already contains this user
    usersJson = open((str(sys.path[0]))+"/data/trackedUsers.json", "r")
    data = json.load(usersJson)
    print("done")
    if user.username in data:
        return True
    else:
        return False
        
    
def convertUserToDictionary(user):
    pass


################

# EXTEND USERS POOL

def extendFollowingUsersPoolFromSuggested(userid, client):
    list = getSuggestedUsersFromFBSearch(userid, client)
    newusers={}
    for usersh in list:
        user = getUserInfoByUsername((convertUserShortToUserv2(usersh, client).username),client)
        if isProfilePrivate(user) == False:
            if isAlreadyTracked(user) == False:
                newusers = trackUser(user, client, newusers)
    if newusers:
        writeNewUsersToJSONFile(newusers)


def extendFollowingUsersPoolFromPostTaggedUsers(post,client):
    list = getPostTaggedPeople(post)
    newusers={}
    for usertag in list:
        usersh=convertUsertagToUser(usertag)
        user = getUserInfoByUsername((convertUserShortToUser(usersh, client).username),client)
        if isProfilePrivate(user) == False:
            if isAlreadyTracked(user) == False:
                newusers = trackUser(user, client, newusers)
    if newusers:
        writeNewUsersToJSONFile(newusers)



def extendFollowingUsersPoolFromTaggedPostsSection(userid, client):
    list = getProfileTaggedPosts(userid, client)
    newusers={}
    for media in list:
        user=getUserInfoByUsername(getUsernameFromID(userid,client),client)
        if isAlreadyTracked(user) == False:
            if isProfilePrivate(user) == False:
                    newusers = trackUser(user, client, newusers)
    if newusers:
        writeNewUsersToJSONFile(newusers)
    


def extendUsersFollowingPool(post, userid, client):
    #extendFollowingUsersPoolFromPostTaggedUsers(post, client)
    extendFollowingUsersPoolFromTaggedPostsSection(userid, client)
    #extendFollowingUsersPoolFromSuggested(userid, client)
    



        

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
            extendUsersFollowingPool(post, userid, client)

#        if hasTaggedLocation(post):
#            detailedLocationInfo = getDetailedMediaLocationInfo(post, client)
#            print(detailedLocationInfo.category)
#            if detailedLocationInfo.category in restaurant_tags:
#                newrestaurants.append(detailedLocationInfo.dict())

    #print(newrestaurants)
#    writeCrawledDataToJson(newrestaurants)
#    return newrestaurants


#########################



#################################################################

def main():
    client = createLoggedInClient()
    #followedUsers = getUserFollowing(getUserIDfromUsername("foxybyte.swe", client), client)
    usertest = getUserIDfromUsername("marcouderzo", client)
    crawlRestaurantsFromProfilePosts(usertest, client)



################################################################

if __name__ == "__main__":
    main()

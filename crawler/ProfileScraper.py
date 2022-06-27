import os, json, sys
from instagrapi import Client
import instagrapi
from typing import Dict

proxy = 'http://46.105.142.10:7497'

os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy


def createLoggedInClient():  #TODO: handle login_required exception
    client = Client()
    client.login("foxybyte.swe", "Swe_2022")
    #client.dump_settings(str(sys.path[0])+"/data/settingsdump.json")
    #client.load_settings(str(sys.path[0])+"/data/settingsdump.json")
    return client


def resetLoginSettings():
    pass

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
    data = getTrackedUsersFromJSON()
    if user.username in data:
        return True
    else:
        return False

def getTrackedUsersFromJSON():
    filepath = (str(sys.path[0]))+"/data/trackedUsers.json"
    with open(filepath) as usersFile:
        try:
            data = json.load(usersFile)
            return data
        except Exception as e:
            print("Error Loading JSON. Probably Empty File.")
            return False

################

# EXTEND USERS POOL

def extendFollowingUsersPoolFromSuggested(userid, client, limit):
    list = getSuggestedUsersFromFBSearch(userid, client)
    newusers={}
    for usersh in list[0:limit]:
        user = getUserInfoByUsername((convertUserShortToUserv2(usersh, client).username),client)
        if isProfilePrivate(user) == False:
            if isAlreadyTracked(user) == False:
                newusers = trackUser(user, client, newusers)
    if newusers:
        writeNewUsersToJSONFile(newusers)


def extendFollowingUsersPoolFromPostTaggedUsers(post,client, limit):
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



def extendFollowingUsersPoolFromTaggedPostsSection(userid, client, limit):
    list = getProfileTaggedPosts(userid, client)
    newusers={}
    for media in list:
        user=getUserInfoByUsername(getUsernameFromID(userid,client),client)
        if isAlreadyTracked(user) == False:
            if isProfilePrivate(user) == False:
                    newusers = trackUser(user, client, newusers)
    if newusers:
        writeNewUsersToJSONFile(newusers)
    


def extendUsersFollowingPool(post, userid, client, limit):
    #extendFollowingUsersPoolFromPostTaggedUsers(post, client, limit)
    extendFollowingUsersPoolFromTaggedPostsSection(userid, client, limit)
    #extendFollowingUsersPoolFromSuggested(userid, client, limit)
    



        

def writeCrawledDataToJson(locationsData): 
	jsondump= json.dumps(locationsData)
	with open((str(sys.path[0]))+"/data/locations.json", "a") as outfile:
		outfile.write(jsondump)


#####################

# FIND RESTAURANTS

def crawlRestaurantsFromProfilePosts(userid, client, allowExtendUserBase, nPostsAllowed):

    restaurant_tags = ['Restaurant', 'Italian Restaurant','Pub', 'Bar', 'Grocery ', 'Wine', 'Diner', 'Food', 'Meal', 'Breakfast', 'Lunch',
                           'Dinner', 'Cafe', 'Tea Room', 'Hotel', 'Pizza', 'Coffee', 'Bakery', 'Dessert', 'Gastropub',
                           'Sandwich', 'Ice Cream', 'Steakhouse']

    postlist = getUserPosts(userid, client)
    newrestaurants = []
    for post in postlist[0:nPostsAllowed]:
        if allowExtendUserBase and getPostTaggedPeople(post) != None:
            extendUsersFollowingPool(post, userid, client, 2)

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
    #trackedUsers = getTrackedUsersFromJSON()
    #print(trackedUsers)
    allowExtendUserBase = True
    nPostsAllowed = 7

    client = createLoggedInClient()
    userid = getUserIDfromUsername("marcouderzo", client)
    crawlRestaurantsFromProfilePosts(userid, client, allowExtendUserBase, nPostsAllowed)
    
#    trackedUsers = getTrackedUsersFromJSON()    
#        for user in trackedUsers:
#        userid = getUserIDfromUsername("marcouderzo", client)
#        crawlRestaurantsFromProfilePosts(userid, client, allowExtendUserBase, nPostsAllowed)



################################################################

if __name__ == "__main__":
    main()

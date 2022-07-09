import os, json, sys, time
from pprint import pprint
from instagrapi import Client
import instagrapi
from typing import Dict

#proxy = 'http://46.105.142.10:7497'

#os.environ['http_proxy'] = proxy 
#os.environ['HTTP_PROXY'] = proxy
#os.environ['https_proxy'] = proxy
#os.environ['HTTPS_PROXY'] = proxy

def createLoggedInClient():  #TODO: handle login_required exception
    client = Client()
    client.login("foxybyte.swe", "Swe_2022")
    #client.dump_settings(str(sys.path[0])+"/data/settingsdump.json")
    #client.load_settings(str(sys.path[0])+"/data/settingsdump.json")
    return client


#######################################

# OTHER

def resetLoginSettings():
    pass


def getNowTime():
    return time.time()

def updateLastLocationCheckTime(locationpk):
    pass

######################################

# USER GETTERS

def getUsernameFromID(userid, client):
    print("getUsernameFromID")
    return client.username_from_user_id(userid)

def getUserIDfromUsername(username, client):
    print("getUserIDfromUsername")
    return getUserInfoByUsername(username, client).pk
    #return client.user_id_from_username(username)

def getUserInfoByUsername(username, client):
    print("getUserInfoByUsername")
    return client.user_info_by_username_v1(username)

def getUserFollowing(userid, client):
    return client.user_following(userid)

def getUserPosts(userid, client):
    return client.user_medias_v1(userid)

def getSuggestedUsersFromFBSearch(userid, client):
    return client.fbsearch_suggested_profiles(userid)

def isProfilePrivate(user):
    return user.is_private

def getPostTaggedPeople(post):
    return post.usertags

def getUserIDofTagged(userid, client):
    return client.usertag_medias(userid)

def getProfileTaggedPosts(userid, client):
    return client.usertag_medias(userid)


###########################################

 # USER CONVERTERS

def convertUsertagToUser(usertag):
    return usertag.user

def convertUserShortToUser(usershort,client):
    print("convertUserShortToUser")
    return client.user_info_by_username(usershort.username)

def convertUserShortToUserv2(usershort,client):
    print("convertUserShortToUserv2")
    return client.user_info_by_username_v1(usershort["username"])

########################################

# LOCATION GETTERS

def getLocationFromPost(media):
    return media.location

def getLocationPkCode(location):
    return location.pk

def hasTaggedLocation(post):
    return post.location != None   # TODO: Da Testare per il != None

def getDetailedMediaLocationInfo(post, client):  # this works and retrieves all category and other data
    mediainfo = client.media_info_v1(post.pk)
    if mediainfo.location != None:
        return client.location_info((mediainfo.location).pk)
    else:
        return None


################################

# LOCATION TRACKING

def getTrackedLocationsFromJSON():
    filepath = (str(sys.path[0]))+"/data/locations.json"
    with open(filepath) as locationsFile:
        try:
            data = json.load(locationsFile)
            return data
        except Exception as e:
            print(e)
            return None


def writeLocationsToJSON(locations): 
	jsondump= json.dumps(locations)
	with open((str(sys.path[0]))+"/data/locations.json", "w") as outfile:
		outfile.write(jsondump)


def trackLocation(locationdict):
    locationsFromJSON = getTrackedLocationsFromJSON()
    print("tracking location: "+ locationdict["name"])
    locationsFromJSON[locationdict["pk"]]=locationdict
    writeLocationsToJSON(locationsFromJSON)



def isLocationTracked(location):
    data = getTrackedLocationsFromJSON()
    if location.pk in data:
        return True
    else:
        return False

##########################################

# LOCATION

def createLocation(input, coordinates):
    dict = {}
    #dict["LastChecked"]=0 # decomment this in order for time-based queueing to work
    dict["pk"] = input["pk"]
    dict["name"] = input["name"]
    dict["address"] = input["address"]
    dict["coordinates"] = [coordinates["lng"], coordinates["lat"]]
    dict["category"] = input["category"]
    dict["phone"] = input["phone"]
    dict["website"] = input["website"]
    return dict;

def getMediaLocationCoordinates(media):
    coordinates = {'lng': (media.location).lng , 
                    'lat': (media.location).lat }
    return coordinates




###########################################

# USER TRACKING

def writeNewUsersToJSONFile(newusers):
    jsondump= json.dumps(newusers)
    with open((str(sys.path[0]))+"/data/trackedUsers.json", "w") as outfile:
	    outfile.write(jsondump)


def getTrackedUsersFromJSON():
    filepath = (str(sys.path[0]))+"/data/trackedUsers.json"
    with open(filepath) as usersFile:
        try:
            data = json.load(usersFile)
            return data
        except Exception as e:
            print(e)
            return None



def isAlreadyTracked(user): #check if database or file already contains this user
    data = getTrackedUsersFromJSON()
    #print(data)
    if user.username in data:
        return True
    else:
        return False


def trackUser(user, client):
    #=(client.user_info(user.pk)).username
    #username = client.user_info_by_username_v1(username).pk
    username = user.username
    usersfromjson = getTrackedUsersFromJSON()
    print("tracking user: "+ username)
    usersfromjson[username]=user.dict()
    writeNewUsersToJSONFile(usersfromjson)






################

# EXTEND USERS POOL

def extendFollowingUsersPoolFromSuggested(userid, client, limit):
    try:
        list = getSuggestedUsersFromFBSearch(userid, client)
    except Exception as e:
        print(e)
        return
    for usersh in list[0:limit]:
        user = getUserInfoByUsername((convertUserShortToUserv2(usersh, client).username),client)
        if isProfilePrivate(user) == False:
            if isAlreadyTracked(user) == False:
                trackUser(user, client)


def extendFollowingUsersPoolFromPostTaggedUsers(post,client):
    list = getPostTaggedPeople(post)
    for usertag in list:
        usersh=convertUsertagToUser(usertag)
        user = getUserInfoByUsername((convertUserShortToUser(usersh, client).username),client)
        if isProfilePrivate(user) == False:
            if isAlreadyTracked(user) == False:
                trackUser(user, client)



def extendFollowingUsersPoolFromTaggedPostsSection(userid, client, limit):
    list = getProfileTaggedPosts(userid, client)
    for media in list[0:limit]:
        user=getUserInfoByUsername(getUsernameFromID(userid,client),client)
        if isAlreadyTracked(user) == False:
            if isProfilePrivate(user) == False:
                    trackUser(user, client)



#####################

# FIND RESTAURANTS

def crawlRestaurantsFromProfilePosts(userid, client, allowExtendUserBase, nPostsAllowed):

    restaurant_tags = ['Restaurant', 'Italian Restaurant','Pub', 'Bar', 'Grocery ', 'Wine', 'Diner', 'Food', 'Meal', 'Breakfast', 'Lunch',
                           'Dinner', 'Cafe', 'Tea Room', 'Hotel', 'Pizza', 'Coffee', 'Bakery', 'Dessert', 'Gastropub',
                           'Sandwich', 'Ice Cream', 'Steakhouse', 'Pizza place', 'Fast food restaurant', 'Deli']

    postlist = getUserPosts(userid, client)
    if nPostsAllowed > len(postlist):
        nPostsAllowed = len(postlist)
    for post in postlist[0:nPostsAllowed]:
        if hasTaggedLocation(post):
            detailedLocationInfo = getDetailedMediaLocationInfo(post, client)
            print("location is a: "+str(detailedLocationInfo.category))
            if detailedLocationInfo.category in restaurant_tags and isLocationTracked(detailedLocationInfo)==False:
                coordinates = getMediaLocationCoordinates(post)
                trackLocation(createLocation(detailedLocationInfo.dict(), coordinates))
        
        if allowExtendUserBase and getPostTaggedPeople(post) != []:
            print("Now extending User Base")
            print(getPostTaggedPeople(post))
            extendFollowingUsersPoolFromPostTaggedUsers(post, client)
            print("Finished Extending User Base")




#########################



#################################################################

def main():
    allowExtendUserBase = True
    nPostsAllowed = 40

    client = createLoggedInClient()
    #trackedUsers = getTrackedUsersFromJSON()    
    trackedUsers = ["foxybyte.swe"] #tests from our account's posts.
    
    for user in trackedUsers:
        print("MAIN LOOP: " + str(user))
        userid = getUserIDfromUsername(user, client)
        crawlRestaurantsFromProfilePosts(userid, client, allowExtendUserBase, nPostsAllowed)
        if allowExtendUserBase:
            print("Now extending User  (from main)")
            extendFollowingUsersPoolFromTaggedPostsSection(userid, client, 4)
            extendFollowingUsersPoolFromSuggested(userid, client, 4)
            print("Finished Extending User Base (from main)")
        



################################################################

if __name__ == "__main__":
    main()

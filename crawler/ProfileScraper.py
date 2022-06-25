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
    return client.user_follow(userid)

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

def classifyLocationType(location):
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

def getUserIDofTagged():
    pass

def getPostPKCode(post, client):
    pass

def getDetailedMediaLocationInfo(post, client):  # this works and retrieves all category and other data
    mediainfo = client.media_info_v1(post.pk)
    if mediainfo.location != None:
        return client.location_info((mediainfo.location).pk)
    else:
        return None

def compareLocationPksToMatch(locPkFromMI, locPkfromLI):
    pass



################

# EXTEND USERS POOL

def extendFollowingUsersPoolFromSuggested():
    pass

def extendFollowingUsersPoolFromTaggedPeople(list):
    pass

def extendFollowingUsersPoolFromTaggedPostsSection():
    pass


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
            extendFollowingUsersPoolFromTaggedPeople(post)

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

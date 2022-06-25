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
    #print(post.location)
    return post.location != None

def getProfileTaggedPosts(userid, client):
    return client.usertag_medias(userid)


def getPostTaggedPeople(post):
    return post.usertags

def getUserIDofTagged():
    pass

def getPostPKCode(post, client):
    pass

def getDetailedMediaInfoFbSearch(post, client):  # this works and retrieves all category and other data
    mediainfo = client.media_info_v1(post.pk)
    if mediainfo.location != None:
        return client.location_info((mediainfo.location).pk)
    else:
        return None



################

# EXTEND USERS POOL

def extendFollowingUsersPoolFromSuggested():
    pass

def extendFollowingUsersPoolFromTaggedPeople(list):
    pass

def extendFollowingUsersPoolFromTaggedPostsSection():
    pass


#####################

# FIND RESTAURANTS

def crawlRestaurantsFromProfilePosts(userid, client):
    postlist = getUserPosts(userid, client)
    newrestaurants = []
    for post in postlist:
        if getPostTaggedPeople(post) != None:
            extendFollowingUsersPoolFromTaggedPeople(post)

        newrestaurants.append(getDetailedMediaInfoFbSearch(post, client))

        #if(hasTaggedLocation(post)):
         #   newrestaurants.append(client.media_info(post.pk))
    print(newrestaurants)
    #print(postlist)
    return newrestaurants


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

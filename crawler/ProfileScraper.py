import os, json, sys
from instagrapi import Client
import instagrapi
from typing import Dict




def createLoggedInClient():
	client = Client()
	client.login("foxybyte.swe", "Swe_2022")
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
    return client.user_medias(userid)

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
    print(getUsernameFromID(userid))
    newrestaurants = []
    print(postlist)
    for post in postlist:
        #if getPostTaggedPeople(post) != None:
         #   extendFollowingUsersPoolFromTaggedPeople(post)

        if(hasTaggedLocation(post)):
             newrestaurants.append(post.location)
    #print(newrestaurants)


#########################



#################################################################

def main():
    client = createLoggedInClient()
    #followedUsers = getUserFollowing(getUserIDfromUsername("foxybyte.swe", client), client)
    usertest = getUserIDfromUsername("marcouderzo", client)

    print(usertest)
    crawlRestaurantsFromProfilePosts(usertest, client)

    
    # find users: follow major italian influencers, or look for top posts hashtagged with food hashtag and city

    #retrieve users already followed.
    #scrape user: 
    #   get all of user's posts & find the ones with restaurants tagged
    #   if other people are tagged in post and their profile is not private: then follow them.
    #   if there are location-tagged posts in user tagged section: follow profile of post creator
    #   save restaurant location



################################################################

if __name__ == "__main__":
    main()

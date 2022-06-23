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
    return client.userfollowing(userid)

def enablePostNotifications(userid, client): #scrape profile if new posts are posted.
    return client.enable_posts_notifications(userid)

def getUserPosts(userid, client):
    return client.user_medias(userid)



def crawlProfilePosts(profile):
    pass

def classifyLocationType():
    pass






#################################################################

def main():
    client = createLoggedInClient()
    
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


from abc import ABC, abstractmethod
import os, json, sys, time
from InstagrapiUtils import InstagrapiUtils
from user.UserProfileFactory import UserProfileFactory



class UserBaseExtender:

    class ExtendUserBasePolicy(ABC):
        @abstractmethod
        def extendUserBaseByPolicy(self, user, limit):
            pass



    class ExtendUserBaseBySuggestedUsers(ExtendUserBasePolicy):
        def extendUserBaseByPolicy(self, user, limit): 
            try:
                instagrapiUtils = InstagrapiUtils()
                list = instagrapiUtils.getSuggestedUsersFromFBSearch(user.pk)
            except Exception as e:
                print(e)
                return
            if limit > len(list):
                limit = len(list)
            uncheckedUserList = []
            for usersh in list[0:limit]:
                usertmp = instagrapiUtils.convertUserShortToUserv2(usersh)
                username = usertmp.username
                usersugg = instagrapiUtils.getUserInfoByUsername(username).dict()
                usersugg["LatestPostPartialURL"] = ''
                if InstagrapiUtils.isProfilePrivate(usersugg) == False:
                    uncheckedUserList.append(UserProfileFactory.buildFromInstagrapi(usersugg, ""))
            return uncheckedUserList

                    


                    

    class ExtendUserBaseByTaggedUsers(ExtendUserBasePolicy):
        def extendUserBaseByPolicy(self, user, limit):
            instagrapiUtils = InstagrapiUtils() 
            posts = instagrapiUtils.getUserPosts(user)
            uncheckedUserList = []
            for post in posts:
                list = instagrapiUtils.getPostTaggedPeople(post)
                for usertag in list:
                    if limit == 0:
                        return
                    usersh=instagrapiUtils.convertUsertagToUser(usertag)
                    usertagged = (instagrapiUtils.getUserInfoByUsername(usersh.username)).dict()
                    #usertagged = (InstagrapiUtils.GetUserInfoByUsername(usersh.username)).dict()
                    user["LatestPostPartialURL"] = ''
                    if instagrapiUtils.isProfilePrivate(usertagged) == False:
                        uncheckedUserList.append(UserProfileFactory.buildFromInstagrapi(usertagged, ""))
                        limit = limit-1
            return uncheckedUserList




    class ExtendUserBaseByTaggedPostsSection(ExtendUserBasePolicy):
        def extendUserBaseByPolicy(self, user, limit): 
            instagrapiUtils = InstagrapiUtils() 
            list = instagrapiUtils.getProfileTaggedPosts(user.pk)
            if list == []:
                print("No posts available in Tagged Posts Section")
            uncheckedUserList = []
            for media in list[0:limit]:
                userposter=instagrapiUtils.getUserInfoByUsername(media.user.username).dict()
                user["LatestPostPartialURL"] = ''
                if self.isAlreadyTracked(userposter) == False:
                    if instagrapiUtils.isProfilePrivate(userposter) == False:
                        uncheckedUserList.append(UserProfileFactory.buildFromInstagrapi(userposter, ""))
            return uncheckedUserList




 

from abc import ABC, abstractmethod
import os, json, sys, time
from InstagrapiUtils import InstagrapiUtils



class UserBaseExtender:
    ##################### WRITING TO JSON ##########################


    class ExtendUserBasePolicy(ABC):
        @abstractmethod
        def extendUserBaseByPolicy(self, user, limit):
            pass



    class ExtendUserBaseBySuggestedUsers(ExtendUserBasePolicy):
        def extendUserBaseByPolicy(self, user, limit): 
            try:
                list = InstagrapiUtils.getSuggestedUsersFromFBSearch(user.pk)
            except Exception as e:
                print(e)
                return
            if limit > len(list):
                limit = len(list)
            uncheckedUserList = []
            for usersh in list[0:limit]:
                usertmp = InstagrapiUtils.convertUserShortToUserv2(usersh)
                username = usertmp.username
                usersugg = InstagrapiUtils.getUserInfoByUsername(username).dict()
                usersugg["LatestPostPartialURL"] = ''
                if InstagrapiUtils.isProfilePrivate(usersugg) == False:
                    uncheckedUserList.append(usersugg)
                    


                    

    class ExtendUserBaseByTaggedUsers(ExtendUserBasePolicy):
        def extendUserBaseByPolicy(self, user, limit): 
            posts = InstagrapiUtils.getUserPosts(user)
            uncheckedUserList = []
            for post in posts:
                list = InstagrapiUtils.getPostTaggedPeople(post)
                for usertag in list:
                    usersh=InstagrapiUtils.convertUsertagToUser(usertag)
                    usertagged = (InstagrapiUtils.getUserInfoByUsername(usersh.username)).dict()
                    #usertagged = (InstagrapiUtils.GetUserInfoByUsername(usersh.username)).dict()
                    user["LatestPostPartialURL"] = ''
                    if InstagrapiUtils.isProfilePrivate(usertagged) == False:
                        uncheckedUserList.append(usertagged)




    class ExtendUserBaseByTaggedPostsSection(ExtendUserBasePolicy):
        def extendUserBaseByPolicy(self, user, limit): 
            list = InstagrapiUtils.getProfileTaggedPosts(user)
            if list == []:
                print("No posts available in Tagged Posts Section")
            uncheckedUserList = []
            for media in list[0:limit]:
                userposter=InstagrapiUtils.getUserInfoByUsername(media.user.username).dict()
                user["LatestPostPartialURL"] = ''
                if self.isAlreadyTracked(userposter) == False:
                    if InstagrapiUtils.isProfilePrivate(userposter) == False:
                            uncheckedUserList.append(userposter)




 
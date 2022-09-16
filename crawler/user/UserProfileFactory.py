from UserProfile import UserProfile
from instagrapi import types

import sys

sys.path.insert(1, (str(sys.path[0]))+"/user/")

class UserProfileFactory:
	
    @staticmethod
    def buildFromInstagrapi(user: types.User, lastpostcheckedcode: str):
        return UserProfile( int(user.pk),
						    user.username,
						    user.is_private,
						    lastpostcheckedcode)


    @staticmethod
    def buildFromDB(user: dict):
        return UserProfile( user['pk'],
                            user['username'],
                            user['isPrivate'],
                            user['lastPostCheckedCode'])
    
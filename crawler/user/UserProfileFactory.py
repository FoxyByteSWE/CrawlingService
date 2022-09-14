from UserProfile import UserProfile
from instagrapi import types

import sys

sys.path.insert(1, (str(sys.path[0]))+"/user/")

class UserProfileFactory:
	
    @staticmethod
    def buildFromInstagrapi(self, user: types.User, lastpostcheckedcode: str):
        return UserProfile( int(user.pk),
						    user.username,
						    user.is_private,
						    lastpostcheckedcode)


    def buildFromDatabase(self, user: dict):
        return UserProfile( user.pk,
                            user.username,
                            user.isprivate,
                            user.lastpostcheckedcode)
    
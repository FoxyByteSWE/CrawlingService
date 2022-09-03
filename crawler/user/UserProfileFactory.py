from UserProfile import UserProfile

class UserProfileFactory:
	
    @staticmethod
    def buildFromInstagrapi(pk: int, username: str, isprivate: bool, lastpostcheckedcode: str):
        return UserProfile( pk,
						    username,
						    isprivate,
						    lastpostcheckedcode)


    def buildFromDatabase(pk: int, username: str, isprivate: bool, lastpostcheckedcode: str):
        return UserProfile( pk,
                            username,
                            isprivate,
                            lastpostcheckedcode)
    
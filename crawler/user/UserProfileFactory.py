from UserProfile import UserProfile

class UserProfileFactory:
	
    @staticmethod
    def buildFromInstagrapiMediaAndLocation(pk: int, username: str, isprivate: bool, lastpostcheckedcode: str):
        return UserProfile( pk,
						    username,
						    isprivate,
						    lastpostcheckedcode)
    
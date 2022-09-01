class UserProfile:
    
    def __init__(self, pk = 0, username = "", isprivate = False, lastpostcheckedcode = "") -> None:
        self.pk = pk
        self.username = username
        self.isPrivate = isprivate
        self.lastPostCheckedCode = lastpostcheckedcode


    def getPk(self) -> int:
        return self.pk

    def getUsername(self) -> str:
        return self.username

    def getIsPrivate(self) -> bool:
        return self.isPrivate

    def getLastPostCheckedCode(self) -> str:
        return self.lastPostCheckedCode

    def setLastPostCheckedCode(self, newcode: str) -> None:
        self.lastPostCheckedCode = newcode
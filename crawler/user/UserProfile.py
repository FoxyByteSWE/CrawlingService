class UserProfile:
    
    def __init__(self, pk = 0, username = "", isprivate = False, lastpostcheckedcode = "") -> None:
        self.pk = pk
        self.username = username
        self.isPrivate = isprivate
        self.lastPostCheckedCode = lastpostcheckedcode


    def convertToDict(self):
        item={}
        item['pk']=self.pk
        item['username']=self.username
        item['isPrivate']=self.isPrivate
        item['lastPostCheckedCode']=self.lastPostCheckedCode
        return item

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
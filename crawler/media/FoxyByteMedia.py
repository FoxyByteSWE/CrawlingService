class FoxyByteMedia:

	def __init__(self, PostPartialURL = "", MediaType = 1, authoruser = "", TakenAtTime = [], TakenAtLocation = {}, LikeCount = 0, CaptionText = "", MediaURLs = [""]):
		self.PostPartialURL = PostPartialURL
		self.MediaType = MediaType
		self.AuthorUsername = authoruser
		self.TakenAtTime = TakenAtTime
		self.TakenAtLocation = TakenAtLocation
		self.LikeCount = LikeCount
		self.CaptionText = CaptionText
		self.MediaURLs = MediaURLs

	
	def convertToDict(self):
		item = {}
		item['PostPartialURL']=self.PostPartialURL
		item['MediaType']=self.MediaType
		item['AuthorUsername']=self.AuthorUsername
		item['TakenAtTime']=self.TakenAtTime
		item['TakenAtLocation']=self.TakenAtLocation
		item['LikeCount']=self.LikeCount
		item['CaptionText']=self.CaptionText
		item['MediaURLs']=self.convertMediaURLsToUniqueString(self.MediaURLs)
		return item

	def convertMediaURLsToUniqueString(self, inputlist: list) -> str:
		string = ""
		for item in inputlist:
			string += item
			string += "|"
		string= string[:-1]
		return string

	def convertMediaUniqueStringToMediaURLs(inputstring) -> list[str]:
		newlist = []
		newlist = inputstring.split("|")
		return newlist

	def getPostPartialURL(self) -> str:
		return self.PostPartialURL

	def getMediaType(self) -> int:
		return self.MediaType

	def getAuthorUsername(self) -> str:
		return self.AuthorUsername

	def getCaptionText(self) -> str:
		return self.CaptionText
	
	def getTakenAtTime(self) -> list:
		return self.TakenAtTime

	def getTakenAtLocation(self) -> dict:
		return self.TakenAtLocation

	def getLikeCount(self) -> int:
		return self.LikeCount

	def getMediaURLs(self) -> list[str]:
		return self.MediaURLs
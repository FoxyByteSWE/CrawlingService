class FoxyByteMedia:

	def __init__(self, PostPartialURL = "", MediaType = 1, authoruser = "", TakenAtTime = [], TakenAtLocation = {}, LikeCount = 0, CaptionText = "", MediaURL = ""):
		self.PostPartialURL = PostPartialURL
		self.MediaType = MediaType
		self.AuthorUsername = authoruser # might as well pass our own User Object
		self.TakenAtTime = TakenAtTime # media
		self.TakenAtLocation = TakenAtLocation
		self.LikeCount = LikeCount
		self.CaptionText = CaptionText
		self.MediaURL = MediaURL

	
	def convertToDict(self):
		item = {}
		item['PostPartialURL']=self.PostPartialURL
		item['MediaType']=self.MediaType
		item['AuthorUsername']=self.AuthorUsername
		item['TakenAtTime']=self.TakenAtTime
		item['TakenAtLocation']=self.TakenAtLocation
		item['LikeCount']=self.LikeCount
		item['CaptionText']=self.CaptionText
		item['MediaURL']=self.MediaURL
		return item

	def getPostPartialURL(self) -> str:
		return self.PostPartialURL

	def getMediaType(self) -> int:
		return self.MediaType

	def getAuthorUsername(self) -> str:
		return self.AuthorUsername

	def getCaptionText(self) -> str:
		return self.CaptionText
	
	def getTakenAtTIme(self) -> list:
		return self.TakenAtTime

	def getTakenAtLocation(self) -> dict:
		return self.TakenAtLocation

	def getLikeCount(self) -> int:
		return self.LikeCount

	def getMediaURL(self) -> str:
		return self.MediaURL
	
	

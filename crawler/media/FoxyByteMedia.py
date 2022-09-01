class FoxyByteMedia:

	def __init__(self, PostPartialURL = "", MediaType = 1, authoruser = "", TakenAtTime = [], TakenAtLocation = {}, LikeCount = 0, CaptionText = "", MediaURL = ""):
		self.PostPartialURL = PostPartialURL
		self.MediaType = MediaType
		self.AuthorUser = authoruser # might as well pass our own User Object
		self.TakenAtTime = TakenAtTime
		self.TakenAtLocation = TakenAtLocation
		self.LikeCount = LikeCount
		self.CaptionText = CaptionText
		self.MediaURL = MediaURL

	
	def getPostPartialURL(self) -> str:
		return self.PostPartialURL

	def getMediaType(self) -> int:
		return self.MediaType
	
	def getTakenAtTIme(self) -> list:
		return self.TakenAtTime

	def getTakenAtLocation(self) -> dict:
		return self.TakenAtLocation

	def getLikeCount(self) -> int:
		return self.LikeCount

	def getMediaURL(self) -> str:
		return self.MediaURL
	
	

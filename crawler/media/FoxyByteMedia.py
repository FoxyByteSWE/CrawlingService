import datetime
	
class FoxyByteMedia:

	def __init__(self, PostPartialURL = "", MediaType = 1, TakenAtTime = [], TakenAtLocation = {}, LikeCount = 0, CaptionText = "", MediaURL = ""):
		self.PostPartialURL = PostPartialURL
		self.MediaType = MediaType
		self.TakenAtTime = TakenAtTime
		self.TakenAtLocation = TakenAtLocation
		self.LikeCount = LikeCount
		self.CaptionText = CaptionText
		self.MediaURL = MediaURL

	
	def getPostPartialURL(self):
		return self.PostPartialURL

	def getMediaType(self):
		return self.MediaType
	
	def getTakenAtTIme(self):
		return self.TakenAtTime

	def getTakenAtLocation(self):
		return self.TakenAtLocation

	def getLikeCount(self):
		return self.LikeCount

	def getMediaURL(self):
		return self.MediaURL

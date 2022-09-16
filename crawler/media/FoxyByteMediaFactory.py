from instagrapi.types import Media
from FoxyByteMedia import FoxyByteMedia


class FoxyByteMediaFactory:

	@staticmethod
	def buildFromInstagrapiMediaAndLocation(media: Media, parsedTakenAt: list, parsedLocation: dict, parsedUrl: str):
		return FoxyByteMedia(media.code,
							media.media_type,
							media.user.username,
							parsedTakenAt, 
							parsedLocation, 
							media.like_count, 
							media.caption_text, 
							parsedUrl) 

	@staticmethod
	def buildFromDB(media: dict):
		return FoxyByteMedia(media["PostPartialURL"],
							media['MediaType'],
							media['AuthorUsername'],
							media["TakenAtTime"], 
							media["TakenAtLocation"], 
							media["LikeCount"],
							media["CaptionText"],
							media["MediaURL"])


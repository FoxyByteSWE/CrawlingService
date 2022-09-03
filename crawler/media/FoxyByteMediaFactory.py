from instagrapi.types import Media
from FoxyByteMedia import FoxyByteMedia


class FoxyByteMediaFactory:

	@staticmethod
	def buildFromInstagrapiMediaAndLocation(media: Media, parsedTakenAt: list, parsedLocation: dict, parsedUrl: str):
		return FoxyByteMedia(media.code, 
							parsedTakenAt, 
							parsedLocation, 
							media.like_count, 
							media.caption_text, 
							parsedUrl) 

	@staticmethod
	def buildFromDB(media: dict):
		return FoxyByteMedia(media["code"],
							media["parsedTakenAt"], 
							media["parsedLocation"], 
							media["like_count"],
							media["caption_text"],
							media["parsedUrl"])


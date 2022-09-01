from instagrapi.types import Media
from FoxyByteMedia import FoxyByteMedia


class FoxyByteMediaFactory:
	
    @staticmethod
    def buildFromInstagrapiMediaAndLocation(media: Media, parsedTakenAt: list, parsedLocation: dict, parsedUrl: str):
        return FoxyByteMedia(media.code,
							parsedTakenAt, #parsed
							parsedLocation, #parsed
							media.like_count,
							media.caption_text,
							parsedUrl) # parsed
		
		

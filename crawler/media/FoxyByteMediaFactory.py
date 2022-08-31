from instagrapi.types import Media

from FoxyByteMedia import FoxyByteMedia


class FoxyByteMediaFactory:
	
    @staticmethod
    def buildFromInstagrapiMedia(media: Media):
        return FoxyByteMedia(media.code,
							media.taken_at, #parse
							media.location, #parse
							media.like_count,
							media.caption_text,
							media.url # parse
		
		

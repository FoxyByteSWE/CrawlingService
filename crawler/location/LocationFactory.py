from Location import Location
from instagrapi.types import Location as InstagrapiLocation


class LocationFactory:

    @staticmethod
    def buildLocationFromInstagrapi(self, instagrapiLocation: InstagrapiLocation, main_image_url, coordinates, latest_post_partial_url_checked) -> Location:
        return Location(instagrapiLocation.pk,
                        instagrapiLocation.name,
                        instagrapiLocation.category,
                        instagrapiLocation.address,
                        instagrapiLocation.website,
                        instagrapiLocation.phone,
                        main_image_url,
                        coordinates,
                        latest_post_partial_url_checked)

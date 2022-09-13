import sys


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


    @staticmethod
    def buildLocationFromDB(self, dbLocation: dict) -> Location:
        return Location(dbLocation["pk"],
                        dbLocation["name"],
                        dbLocation["category"],
                        dbLocation["address"],
                        dbLocation["website"],
                        dbLocation["phone"],
                        dbLocation["main_image_url"],
                        dbLocation["coordinates"],
                        dbLocation["latest_post_partial_url_checked"])

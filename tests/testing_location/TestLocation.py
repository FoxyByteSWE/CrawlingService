import unittest
from unittest.mock import patch
import sys,os

from crawler.location.Location import Location



class TestLocation(unittest.TestCase):
    def setUp(self):

        self.location = Location(12345,
                            "Lunaelaltro",
                            "Pizzeria",
                            "Corso della Ceramica, 33, 36063 Marostica VI",
                            "www.lunaelaltro.it",
                            "123456789",
                            "www.thisissomelink.to/imageurl",
                            {"lng": 1.111, "lat": 2.222},
                            "12AB34CD")

    
    def test_convertToDict(self):
        self.assertEqual(self.location.convertToDict(),({"pk": 12345,
                                                    "name": "Lunaelaltro",
                                                    "category": "Pizzeria",
                                                    "address": "Corso della Ceramica, 33, 36063 Marostica VI",
                                                    "website": "www.lunaelaltro.it",
                                                    "phone": "123456789",
                                                    "main_image_url": "www.thisissomelink.to/imageurl",
                                                    "coordinates": {"lng": 1.111, "lat": 2.222},
                                                    "latest_post_partial_url_checked": "12AB34CD"}))



    def test_getPk(self):
        return self.assertEqual(self.location.pk, 12345)

    def test_getName(self):
        return self.assertEqual(self.location.name, "Lunaelaltro")

    def test_getCategory(self):
        return self.assertEqual(self.location.category, "Pizzeria")

    def test_getAddress(self):
        return self.assertEqual(self.location.address, "Corso della Ceramica, 33, 36063 Marostica VI")

    def test_getCoordinates(self):
        return self.assertEqual(self.location.coordinates, {"lng": 1.111, "lat": 2.222})

    def test_getWebsite(self):
        return self.assertEqual(self.location.website, "www.lunaelaltro.it")

    def test_getPhone(self):
        return self.assertEqual(self.location.phone, "123456789")

    def test_getMainImageUrl(self):
        return self.assertEqual(self.location.main_image_url, "www.thisissomelink.to/imageurl")

    def test_getLatestPostPartialURLChecked(self):
        return self.assertEqual(self.location.latest_post_partial_url_checked, "12AB34CD")

    def test_setLatestPostPartialUrlChecked(self):
        self.location.setLatestPostPartialUrlChecked("newcode")
        return self.assertEqual(self.location.latest_post_partial_url_checked, "newcode")
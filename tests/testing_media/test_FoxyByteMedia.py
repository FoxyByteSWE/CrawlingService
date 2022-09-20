import unittest
from unittest.mock import patch
import sys,os

sys.path.insert(1, (str(sys.path[0]))+"/../../crawler/media/")
from FoxyByteMedia import FoxyByteMedia


class TestFoxyByteMedia(unittest.TestCase):
    def setUp(self):

        self.maxDiff = None

        self.media = FoxyByteMedia("ABCDE123",
                                    1,
                                    "marcouderzo",
                                    [2022, 9, 9, 17, 20, 0],
                                    {"pk": 12345,
                                    "name":  "Lunaelaltro",
                                    "category": "Pizzeria",
                                    "address": "Corso della Ceramica, 33, 36063 Marostica VI",
                                    "website": "www.lunaelaltro.it",
                                    "phone": "123456789",
                                    "main_image_url": "www.thisissomelink.to/imageurl",
                                    "coordinates": {"lng": 1.111, "lat": 2.222},
                                    "latest_post_partial_url_checked": "12AB34CD"},
                                    123,
                                    "this is a caption text",
                                    ["somelinktomedia/aaaaaaaa"])

        self.Albummedia = FoxyByteMedia("ABCDE123",
                                    8,
                                    "marcouderzo",
                                    [2022, 9, 9, 17, 20, 0],
                                    {"pk": 12345,
                                    "name":  "Lunaelaltro",
                                    "category": "Pizzeria",
                                    "address": "Corso della Ceramica, 33, 36063 Marostica VI",
                                    "website": "www.lunaelaltro.it",
                                    "phone": "123456789",
                                    "main_image_url": "",
                                    "coordinates": {"lng": 1.111, "lat": 2.222},
                                    "latest_post_partial_url_checked": "12AB34CD"},
                                    123,
                                    "this is a caption text",
                                    ["somelinktomedia/aaaaaaaa",
                                    "someotherlinktomedia/bbbbbbb"])



    def test_convertToDict(self):
        self.assertEqual(self.media.convertToDict(), {"PostPartialURL": "ABCDE123",
                                                        "MediaType": 1,
                                                        "AuthorUsername": "marcouderzo",
                                                        "TakenAtTime": [2022, 9, 9, 17, 20, 0],
                                                        "TakenAtLocation": {"pk": 12345,
                                                                            "name": "Lunaelaltro",
                                                                            "category": "Pizzeria",
                                                                            "address": "Corso della Ceramica, 33, 36063 Marostica VI",
                                                                            "website": "www.lunaelaltro.it",
                                                                            "phone": "123456789",
                                                                            "main_image_url": "www.thisissomelink.to/imageurl",
                                                                            "coordinates": {"lng": 1.111, "lat": 2.222},
                                                                            "latest_post_partial_url_checked": "12AB34CD"},
                                                        "LikeCount": 123,
                                                        "CaptionText": "this is a caption text",
                                                        "MediaURLs": "somelinktomedia/aaaaaaaa"})

    def test_convertToDict_Album(self):
        self.assertEqual(self.Albummedia.convertToDict(), {"PostPartialURL": "ABCDE123",
                                                        "MediaType": 8,
                                                        "AuthorUsername": "marcouderzo",
                                                        "TakenAtTime": [2022, 9, 9, 17, 20, 0],
                                                        "TakenAtLocation": {"pk": 12345,
                                                                            "name": "Lunaelaltro",
                                                                            "category": "Pizzeria",
                                                                            "address": "Corso della Ceramica, 33, 36063 Marostica VI",
                                                                            "website": "www.lunaelaltro.it",
                                                                            "phone": "123456789",
                                                                            "main_image_url": "",
                                                                            "coordinates": {"lng": 1.111, "lat": 2.222},
                                                                            "latest_post_partial_url_checked": "12AB34CD"},
                                                        "LikeCount": 123,
                                                        "CaptionText": "this is a caption text",
                                                        "MediaURLs": "somelinktomedia/aaaaaaaa|someotherlinktomedia/bbbbbbb"})

    


    def test_getPostPartialURL(self):
        self.assertEqual(self.media.getPostPartialURL(), "ABCDE123")

    def test_getMediaType(self):
        self.assertEqual(self.media.getMediaType(), 1)
    
    def test_getTakenAtTime(self):
        self.assertEqual(self.media.getTakenAtTime(), [2022, 9, 9, 17, 20, 0])  

    def test_getAuthorUsername(self):
        self.assertEqual(self.media.getAuthorUsername(), "marcouderzo")

    def test_getMediaType(self):
        self.assertEqual(self.media.getMediaType(), 1)

    def test_getTakenAtLocation(self):
        self.assertEqual(self.media.getTakenAtLocation(), {"pk": 12345,
                                                            "name": "Lunaelaltro",
                                                            "category": "Pizzeria",
                                                            "address": "Corso della Ceramica, 33, 36063 Marostica VI",
                                                            "website": "www.lunaelaltro.it",
                                                            "phone": "123456789", 
                                                            "main_image_url": "www.thisissomelink.to/imageurl",
                                                            "coordinates": {"lng": 1.111, "lat": 2.222},
                                                            "latest_post_partial_url_checked": "12AB34CD"})

    def test_getLikeCount(self):
        self.assertEqual(self.media.getLikeCount(), 123)

    def test_getMediaURLs(self):
        self.assertEqual(self.media.getMediaURLs(), ["somelinktomedia/aaaaaaaa"])
    

    
unittest.main()
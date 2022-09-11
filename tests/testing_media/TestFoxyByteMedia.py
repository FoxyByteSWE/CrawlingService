import unittest
from unittest.mock import patch
import sys,os

from crawler.media.FoxyByteMedia import FoxyByteMedia


class TestUserProfile(unittest.TestCase):
    def setUp(self):

        self.media = FoxyByteMedia("ABCDE123",
                                    1,
                                    "marcouderzo",
                                    [2022, 9, 9, 17, 20, 0],
                                    {1: "TODO LOCATION"},
                                    123,
                                    "this is a caption text",
                                    "somelinktomedia/aaaaaaaa")



    def test_convertToDict(self):
        self.assertEqual(self.media.convertToDict(), {"PostPartialURL": "ABCDE123",
                                                        "MediaType": 1,
                                                        "AuthorUsername": "marcouderzo",
                                                        "TakenAtTime": [2022, 9, 9, 17, 20, 0],
                                                        "TakenAtLocation": {1: "TODO LOCATION"},
                                                        "LikeCount": 123,
                                                        "CaptionText": "this is a caption text",
                                                        "MediaURL": "somelinktomedia/aaaaaaaa"})

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
        self.assertEqual(self.media.getTakenAtLocation(), {1: "TODO LOCATION"})

    def test_getLikeCount(self):
        self.assertEqual(self.media.getLikeCount(), 123)

    def test_getMediaURL(self):
        self.assertEqual(self.media.getMediaURL(), "somelinktomedia/aaaaaaaa")
    

    

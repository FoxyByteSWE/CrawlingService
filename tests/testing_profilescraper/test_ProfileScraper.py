import unittest
from unittest.mock import patch
import sys

sys.path.insert(1, (str(sys.path[0]))+"/../../crawler/")

from ProfileScraper import ProfileScraper
from InstagrapiUtils import InstagrapiUtils



class TestProfileScraper(unittest.TestCase):
    def setUp(self):
        self.profileScraper = ProfileScraper()


    def test_checkIfPostIsNew(self):
        self.assertFalse(self.profileScraper.checkIfPostIsNew("123", 123))


    def test_checkIfPostIsNew(self):
        self.assertFalse(self.profileScraper.checkIfPostIsNew("123", "123"))



    def test_checkIfPostIsNew(self):
        with patch('db.executeQuery') as mockQueryResponse:
            mockQueryResponse.return_value = False
            with patch('crawler.user.UserProfile.__init__') as mockUser:
                self.profileScraper.isAlreadyTracked(mockUser)
    
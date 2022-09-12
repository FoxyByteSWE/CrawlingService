import unittest
from unittest.mock import patch

sys.path.insert(1, (str(sys.path[0]))+"/../../")
from crawler.ProfileScraper import ProfileScraper
from crawler.InstagrapiUtils import InstagrapiUtils
from crawler.user.UserProfile import UserProfile



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
    
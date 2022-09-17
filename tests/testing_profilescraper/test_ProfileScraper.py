import unittest
from unittest.mock import patch
import sys

sys.path.insert(1, (str(sys.path[0]))+"/../../crawler/")
sys.path.insert(1, (str(sys.path[0]))+"/data")
sys.path.insert(1, (str(sys.path[0]))+"/../../crawler/location")
sys.path.insert(1, (str(sys.path[0]))+"/../../crawler/user")

from ProfileScraper import ProfileScraper
from InstagrapiUtils import InstagrapiUtils
from DBConnection import DBConnection



class TestProfileScraper(unittest.TestCase):
    def setUp(self):
        with patch('InstagrapiUtils.__init__') as instagrapiInit:
            instagrapiInit.side_effect = None
            with patch('DBConnection.__init__') as dbInit:
                dbInit.side_effect = None
                self.profileScraper = ProfileScraper()

    def test_checkIfPostIsNew(self):
        return self.assertFalse(self.profileScraper.checkIfPostIsNew("123", "123"))



#    def test_checkIfPostIsNew(self):
#        with patch('DBConnection.executeQuery') as mockQueryResponse:
#            mockQueryResponse.return_value = False
#            with patch('crawler.user.UserProfile.__init__') as mockUser:
#                self.profileScraper.isAlreadyTracked(mockUser)
    

unittest.main()
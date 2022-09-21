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



    def test_isUserAlreadyTracked(self):
        with patch('DBConnection.__init__'):
            with patch('DBConnection.executeQuery') as mockQueryResponse:
                mockQueryResponse.return_value = None
                with patch('crawler.user.UserProfile.__init__') as mockUser:
                    self.assertFalse(self.profileScraper.isAlreadyTracked(mockUser))
    

    def test_get_media(self):
        with patch('crawler.Crawler.Crawler.get_id_from_username') as mock_get_id_from_username, \
                patch('instagrapi.Client.user_medias_v1') as mock_user_medias_v1:
            mock_get_id_from_username.return_value = 4213
            mock_user_medias_v1.return_value = 'media'
            self.assertEqual(self.crawler.get_media('username'), 'media')

unittest.main()
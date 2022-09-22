import unittest
from unittest.mock import patch


import sys
sys.path.insert(1, (str(sys.path[0]))+"/../../crawler/")
sys.path.insert(1, (str(sys.path[0]))+"/../../crawler/media")
from Crawler import Crawler




class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.crawler = Crawler()


    def test_isMediaDuplicated(self):
        with patch('DBConnection.DBConnection.executeQuery') as mock_exec_query, \
            patch('media.FoxyByteMedia.FoxyByteMedia') as mock_media:
                mock_exec_query.return_value = None
                mock_media.return_value = 'media'
                self.assertFalse(self.crawler.isMediaDuplicated(mock_media))

    def test_checkIfPostIsNew(self):
        self.assertTrue(self.crawler.checkIfPostIsNew("ABC123", "ABC123"))

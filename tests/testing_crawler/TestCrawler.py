import unittest
from unittest.mock import patch

from crawler.Crawler import Crawler
from crawler.InstagrapiUtils import InstagrapiUtils
from crawler.user.UserProfile import UserProfile



class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.crawler = Crawler()
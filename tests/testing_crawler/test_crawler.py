import unittest
from unittest.mock import patch


import sys
sys.path.insert(1, (str(sys.path[0]))+"/../../crawler/")
sys.path.insert(1, (str(sys.path[0]))+"/../../crawler/media")
from Crawler import Crawler




class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.crawler = Crawler()
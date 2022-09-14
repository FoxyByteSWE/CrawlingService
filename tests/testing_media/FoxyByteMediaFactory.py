import unittest
from unittest.mock import patch
import sys,os

from instagrapi import types


sys.path.insert(1, (str(sys.path[0]))+"/../../")
from crawler.media.FoxyByteMediaFactory import FoxyByteMediaFactory
from crawler.media.FoxyByteMedia import FoxyByteMedia



class TestFoxyByteMediaFactory(unittest.TestCase):
    def setUp(self):
        self.testFoxyByteMedia = FoxyByteMedia() # TODO: pass params
        
        self.testInstagrapiMedia = types.Media() # TODO: pass params

        self.testDBDictMedia =  {} # TODO: pass params


    def test_buildFromInstagrapiMediaAndLocation(self):
        self.assertEqual(FoxyByteMediaFactory.buildFromInstagrapiMediaAndLocation(self.testInstagrapiMedia, ["parsedTakenAt"], {1: "parsedlocation"}, "parsedurl"), self.testFoxyByteMedia) # TODO: pass params


    def test_buildFromDB(self):
        self.assertEqual(FoxyByteMediaFactory.buildFromDB(self.testDBDictMedia), self.testFoxyByteMedia)


unittest.main()
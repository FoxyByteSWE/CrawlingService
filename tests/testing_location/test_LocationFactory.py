import unittest
from unittest.mock import patch
import sys,os

from instagrapi import types


sys.path.insert(1, (str(sys.path[0]))+"/../../")
from crawler.location.LocationFactory import LocationFactory
from crawler.location.Location import Location



class TestLocationFactory(unittest.TestCase):
    def setUp(self):
        self.testLocation = LocationFactory() # TODO: pass params
        
        self.testInstagrapiLocation = types.Location() # TODO: pass params

        self.testDBDictLocation =  {} # TODO: pass params


    def test_buildFromInstagrapiMediaAndLocation(self):
        self.assertEqual(LocationFactory.buildFromInstagrapi(self.testInstagrapiLocation, "imageurl", {'lng': 1.1111, 'lat': 2.2222}, "somecode"), self.testLocation) # TODO: pass params


    def test_buildFromDB(self):
        self.assertEqual(LocationFactory.buildFromDB(self.testDBDictLocation), self.testLocation)


unittest.main()
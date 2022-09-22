import unittest
from unittest.mock import patch

import sys
sys.path.insert(1, (str(sys.path[0]))+"/../../crawler/")

from LocationProfileFinder import LocationProfileFinder



class TestLocationProfileFinder(unittest.TestCase):
    def setUp(self):
        pass

    def test_checkForRestaurantUsername(self):
        self.assertTrue(LocationProfileFinder.checkForRestaurantUsername("Ristorante Pizzeria Lunaelaltro", "pizzerialunaelaltro"))
        self.assertFalse(LocationProfileFinder.checkForRestaurantUsername("Ristorante Pizzeria Lunaelaltro", "Pizzeria La Bionda"))


unittest.main()
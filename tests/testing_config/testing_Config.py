import unittest
from unittest import mock
from unittest.mock import patch
import sys

sys.path.insert(1, (str(sys.path[0]))+"/../../")
sys.path.insert(1, (str(sys.path[0]))+"/../../crawler")
from Config import CrawlingServiceConfig

class TestCrawlingServiceConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.loadedJSONDict = {
                                "allowExtendUserBase": "True",
                                "extendUserBasePolicyNumber": 2,
                                "extendUserBasePolicy": 2,
                                "nMaxUsersToAdd": 10,
                                "nPostsAllowedForProfileScraping": 40,
                                "nPostsWantedForEachLocation": 50,
                                "instagramUsername" : "someusername",
                                "instagramPassword" : "somepassword",
                                "locationTags" : ["Restaurant", 
                                                    "Italian Restaurant",
                                                    "Pub", 
                                                    "Bar", 
                                                    "Grocery", 
                                                    "Wine", 
                                                    "Diner", 
                                                    "Food", 
                                                    "Meal", 
                                                    "Breakfast", 
                                                    "Lunch", 
                                                    "Dinner", 
                                                    "Cafe", 
                                                    "Tea Room", 
                                                    "Hotel", 
                                                    "Pizza", 
                                                    "Coffee", 
                                                    "Bakery", 
                                                    "Dessert", 
                                                    "Gastropub",
                                                    "Sandwich", 
                                                    "Ice Cream", 
                                                    "Steakhouse", 
                                                    "Pizza place", 
                                                    "Fast food restaurant", 
                                                    "Deli"]
                            }
    
        
    
    def test_CrawlingServiceConfig(self):
        with patch('Config.CrawlingServiceConfig.readFromJSON') as mock_readFromJSON:
            mock_readFromJSON.return_value = self.loadedJSONDict
            testConfig = CrawlingServiceConfig()
            self.assertEqual(testConfig.allowExtendUserBase, True)
            self.assertEqual(testConfig.extendUserBasePolicyNumber, 2)
            self.assertEqual(testConfig.extendUserBasePolicy, 2)
            self.assertEqual(testConfig.nMaxUsersToAdd, 10)
            self.assertEqual(testConfig.nPostsAllowedForProfileScraping, 40)
            self.assertEqual(testConfig.nPostsWantedForEachLocation, 50)
            self.assertEqual(testConfig.instagramUsername, "someusername")
            self.assertEqual(testConfig.instagramPassword, "somepassword")
            self.assertEqual(testConfig.locationTags, ["Restaurant", 
                                                        "Italian Restaurant",
                                                        "Pub", 
                                                        "Bar", 
                                                        "Grocery", 
                                                        "Wine", 
                                                        "Diner", 
                                                        "Food", 
                                                        "Meal", 
                                                        "Breakfast", 
                                                        "Lunch", 
                                                        "Dinner", 
                                                        "Cafe", 
                                                        "Tea Room", 
                                                        "Hotel", 
                                                        "Pizza", 
                                                        "Coffee", 
                                                        "Bakery", 
                                                        "Dessert", 
                                                        "Gastropub",
                                                        "Sandwich", 
                                                        "Ice Cream", 
                                                        "Steakhouse", 
                                                        "Pizza place", 
                                                        "Fast food restaurant", 
                                                        "Deli"])

        

unittest.main()

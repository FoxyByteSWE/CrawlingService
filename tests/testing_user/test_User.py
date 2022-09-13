import unittest
from unittest.mock import patch
import sys,os


sys.path.insert(1, (str(sys.path[0]))+"/../../")
from crawler.user.UserProfile import UserProfile



class TestUserProfile(unittest.TestCase):
    def setUp(self):

        self.user = UserProfile(12345,
                                "marcouderzo",
                                False,
                                "12AB34CD")

    
    def test_convertToDict(self):
        self.assertEqual(self.user.convertToDict(), {"pk": 12345,
                                                     "username": "marcouderzo",
                                                     "isPrivate": False,
                                                     "lastPostCheckedCode": "12AB34CD" })


    def test_getPk(self):
        self.assertEqual(self.user.getPk(), 12345)

    def test_getUsername(self):
        self.assertEqual(self.user.getUsername(), "marcouderzo")

    def test_getIsPrivate(self):
        self.assertFalse(self.user.getIsPrivate())
    
    def test_getLastPostCheckedCode(self):
        self.assertEqual(self.user.getLastPostCheckedCode(), "12AB34CD")

    def test_setLastPostCheckedCode(self):
        self.user.setLastPostCheckedCode("newcode")
        self.assertTrue(self.user.getLastPostCheckedCode() == "newcode")

    



    


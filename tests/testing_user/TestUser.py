import unittest
from unittest.mock import patch

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
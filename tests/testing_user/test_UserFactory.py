import unittest
from unittest.mock import patch
import sys,os

from instagrapi import types


sys.path.insert(1, (str(sys.path[0]))+"/../../")
from crawler.user.UserProfile import UserProfile
from crawler.user.UserProfileFactory import UserProfileFactory



class TestUserProfile(unittest.TestCase):
    def setUp(self):

        self.testUser = UserProfile(1234, "testuser", False, "somecode")

        self.instagrapiUser = types.User("1234", "testuser", "", False)
  
        self.databaseDictUser = {'pk' : 1234,
                                'username' : "testuser",
                                'isPrivate': False,
                                'lastPostCheckedCode': "somecode"}


    def test_buildFromInstagrapi(self):
        self.assertEqual(UserProfileFactory.buildFromInstagrapi(self.instagrapiUser, "somecode"), self.testUser)


    def test_buildFromDB(self):
        self.assertEqual(UserProfileFactory.buildFromDatabase(self.databaseDictUser), self.testUser)


unittest.main()
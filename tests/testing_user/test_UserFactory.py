import unittest
from unittest.mock import patch
import sys,os

from instagrapi import types


#sys.path.insert(1, (str(sys.path[0]))+"/../../")
#from crawler.user.UserProfile import UserProfile
#from crawler.user.UserProfileFactory import UserProfileFactory


sys.path.insert(1, (str(sys.path[0]))+"/../../crawler/user/")
from UserProfile import UserProfile
from UserProfileFactory import UserProfileFactory



class TestUserProfileFactory(unittest.TestCase):
    def setUp(self):

        self.instagrapiUser = types.User(pk="53184308084",
                                        username="foxybyte.swe",
                                        full_name="FoxyByte", 
                                        is_private=False, 
                                        profile_pic_url="https://instagram.fqpa1-1.fna.fbcdn.net/v/t51.2885-19/281823066_4962293020554259_5303465998407939050_n.jpg?stp=dst-jpg_s150x150&_nc_ht=instagram.fqpa1-1.fna.fbcdn.net&_nc_cat=107&_nc_ohc=X4PNSBFSqsQAX8o0kfR&edm=AKralEIBAAAA&ccb=7-5&oh=00_AT89g6OMnIrCbMD36Z65rKsQFYY1cQ5fyX50Epm4ogS1kw&oe=63123841&_nc_sid=5e3072",
                                        profile_pic_url_hd=None, 
                                        is_verified=False,
                                        media_count=5, 
                                        follower_count=0, 
                                        following_count=3, 
                                        biography="- FoxyByte Automated Account \n- SWE 2021/22 @ UniPD, Group 15", 
                                        external_url="https://github.com/FoxyByteSWE", 
                                        account_type=1, 
                                        is_business=False)

        self.databaseDictUser = {'pk' : 53184308084,
                                'username' : "foxybyte.swe",
                                'isPrivate': False,
                                'lastPostCheckedCode': "somecode"}


    def test_buildFromInstagrapi(self):
        user= UserProfileFactory.buildFromInstagrapi(self.instagrapiUser, "somecode")
        self.assertEqual(user.getIsPrivate(), False)
        self.assertEqual(user.getUsername(), "foxybyte.swe")
        self.assertEqual(user.getLastPostCheckedCode(), "somecode")
        self.assertEqual(user.getPk(), 53184308084)


    def test_buildFromDB(self):
        user= UserProfileFactory.buildFromDB(self.databaseDictUser)
        self.assertEqual(user.getIsPrivate(), False)
        self.assertEqual(user.getUsername(),  "foxybyte.swe")
        self.assertEqual(user.getLastPostCheckedCode(), "somecode")
        self.assertEqual(user.getPk(), 53184308084)


unittest.main()
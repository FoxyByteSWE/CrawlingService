import unittest
from unittest.mock import patch
import os

import sys


from crawler.InstagrapiUtils import InstagrapiUtils


import instagrapi
from instagrapi import types
from instagrapi.types import HttpUrl


import datetime


class TestInstagrapi(unittest.TestCase):
    def setUp(self) -> None:
        self.instagrapiUtils = InstagrapiUtils()


####################################  TEST MEDIA #################################

        self.media = types.Media(pk='2919305163060880463', 
                                id='2919305163060880463_281443894', 
                                code='CiDdJQjNSRP', 
                                taken_at=datetime.datetime(2022, 9, 3, 18, 5, 16, tzinfo=datetime.timezone.utc), 
                                media_type=8, 
                                product_type='carousel_container', 
                                thumbnail_url=None, 
                                location=types.Location(pk=3110887, 
                                                        name='Ristorante Pizzeria Lunaelaltro - Marostica', 
                                                        phone='', 
                                                        website='', 
                                                        category='', 
                                                        hours={}, 
                                                        address=None, 
                                                        city=None, 
                                                        zip=None, 
                                                        lng=11.660707634193, lat=45.736862428411, 
                                                        external_id=77610911328, 
                                                        external_id_source='facebook_places'), 
                                user=types.UserShort(pk='281443894', 
                                                    username='william_lucchin', 
                                                    full_name='William Lucchin', 
                                                    profile_pic_url=HttpUrl('https://instagram.fmxp5-1.fna.fbcdn.net/v/t51.2885-19/220791469_538148194288015_175587587912182841_n.jpg?stp=dst-jpg_s150x150&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=107&_nc_ohc=N-9Qp0Nq5zkAX8jLkC7&edm=AKmAybEBAAAA&ccb=7-5&oh=00_AT-EZH5KaZ0dPby9NKaiSqPKArXsucUFLUuuNDIU5RI5Qg&oe=63229251&_nc_sid=bcb968', 
                                                                            scheme='https', 
                                                                            host='instagram.fmxp5-1.fna.fbcdn.net', 
                                                                            tld='net', 
                                                                            host_type='domain', 
                                                                            port='443', 
                                                                            path='/v/t51.2885-19/220791469_538148194288015_175587587912182841_n.jpg', 
                                                                            query='stp=dst-jpg_s150x150&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=107&_nc_ohc=N-9Qp0Nq5zkAX8jLkC7&edm=AKmAybEBAAAA&ccb=7-5&oh=00_AT-EZH5KaZ0dPby9NKaiSqPKArXsucUFLUuuNDIU5RI5Qg&oe=63229251&_nc_sid=bcb968'), 
                                                    profile_pic_url_hd=None, 
                                                    is_private=False, 
                                                    stories=[]), 
                                comment_count=0, 
                                like_count=4, 
                                has_liked=False, 
                                caption_text='', 
                                accessibility_caption=None, 
                                usertags=[], 
                                video_url=None, 
                                view_count=0, 
                                video_duration=0.0, 
                                title='', 
                                resources=[types.Resource(pk='2919305149119116731', 
                                                        video_url=None, 
                                                        thumbnail_url=HttpUrl('https://instagram.fmxp5-1.fna.fbcdn.net/v/t39.30808-6/302560636_10225220452889775_4354789437307590688_n.jpg?stp=c0.64.1536.1920a_dst-jpg_e35_s1080x1080_sh0.08&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=103&_nc_ohc=pbzOsujR_swAX_Fq5nc&edm=AKmAybEAAAAA&ccb=7-5&ig_cache_key=MjkxOTMwNTE0OTExOTExNjczMQ%3D%3D.2-ccb7-5&oh=00_AT_CMVHHNQjkJyzNJLmCevqu9yU3bJHph5EDe7f0gYtK5g&oe=63239D11&_nc_sid=bcb968', 
                                                                            scheme='https', 
                                                                            host='instagram.fmxp5-1.fna.fbcdn.net', 
                                                                            tld='net', 
                                                                            host_type='domain', 
                                                                            port='443', 
                                                                            path='/v/t39.30808-6/302560636_10225220452889775_4354789437307590688_n.jpg', 
                                                                            query='stp=c0.64.1536.1920a_dst-jpg_e35_s1080x1080_sh0.08&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=103&_nc_ohc=pbzOsujR_swAX_Fq5nc&edm=AKmAybEAAAAA&ccb=7-5&ig_cache_key=MjkxOTMwNTE0OTExOTExNjczMQ%3D%3D.2-ccb7-5&oh=00_AT_CMVHHNQjkJyzNJLmCevqu9yU3bJHph5EDe7f0gYtK5g&oe=63239D11&_nc_sid=bcb968'), 
                                                                            media_type=1), 
                                            types.Resource(pk='2919305148590466507', 
                                                            video_url=None,       
                                                            thumbnail_url=HttpUrl('https://instagram.fmxp5-1.fna.fbcdn.net/v/t39.30808-6/302556896_10225220452969777_3934992198777190024_n.jpg?stp=c0.64.1536.1920a_dst-jpg_e35_s1080x1080_sh0.08&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=101&_nc_ohc=QiQIp85aTTUAX8nCifb&edm=AKmAybEAAAAA&ccb=7-5&ig_cache_key=MjkxOTMwNTE0ODU5MDQ2NjUwNw%3D%3D.2-ccb7-5&oh=00_AT_1fUR5fEttm5S-Rl31TjChM9k1qslnFC3hWJc3KDUELQ&oe=6323D4B5&_nc_sid=bcb968', 
                                                                                    scheme='https',
                                                                                    host='instagram.fmxp5-1.fna.fbcdn.net', 
                                                                                    tld='net', 
                                                                                    host_type='domain', 
                                                                                    port='443', 
                                                                                    path='/v/t39.30808-6/302556896_10225220452969777_3934992198777190024_n.jpg', 
                                                                                    query='stp=c0.64.1536.1920a_dst-jpg_e35_s1080x1080_sh0.08&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=101&_nc_ohc=QiQIp85aTTUAX8nCifb&edm=AKmAybEAAAAA&ccb=7-5&ig_cache_key=MjkxOTMwNTE0ODU5MDQ2NjUwNw%3D%3D.2-ccb7-5&oh=00_AT_1fUR5fEttm5S-Rl31TjChM9k1qslnFC3hWJc3KDUELQ&oe=6323D4B5&_nc_sid=bcb968'), 
                                                            media_type=1)], 
                                clips_metadata={})


################################################################




    def test_loadCookies(self):
        self.assertEqual(self.instagrapiUtils.loadCookies(),
            {"uuids": {"phone_id": "19fd873a-165b-49ce-8fd7-822571400339", 
                        "uuid": "cb5be7f9-5a34-457e-9fbc-bd8583539415", 
                        "client_session_id": "a5583b19-210a-447d-ba35-c71daa196ad0", 
                        "advertising_id": "ea471400-df95-433c-aeef-5ac48de7b414", 
                        "android_device_id": "android-00e13894c1e74e9a", 
                        "request_id": "ebab8430-0023-485e-bc22-d15e53f924bc", 
                        "tray_session_id": "4393b7fe-129b-480c-89fb-b4054214a0f0"}, 
            "mid": "Ywt9aQABAAHjIUa_3NBvy3tfsv9W", 
            "ig_u_rur": "null", 
            "ig_www_claim": "null", 
            "authorization_data": {"ds_user_id": "53184308084", 
                                    "sessionid": "53184308084%3AvpM1UVQYyVyTxm%3A0%3AAYcpmt0QT2Q2LCVHiJ2-g5u4UwFvwlbz8tku88sEsQ"}, 
            "cookies": {}, 
            "last_login": 1661697456.3865955, 
            "device_settings": {"app_version": "203.0.0.29.118", 
                                "android_version": 26, 
                                "android_release": "8.0.0", 
                                "dpi": "480dpi", 
                                "resolution": "1080x1920", 
                                "manufacturer": "Xiaomi", 
                                "device": "capricorn", 
                                "model": "MI 5s", 
                                "cpu": "qcom", 
                                "version_code": "314665256"}, 
            "user_agent": "Instagram 203.0.0.29.118 Android (26/8.0.0; 480dpi; 1080x1920; Xiaomi; MI 5s; capricorn; qcom; en_US; 314665256)", 
            "country": "US", 
            "country_code": 1, 
            "locale": "en_US", 
            "timezone_offset": -14400})




    
    def test_parseTakenAtTime(self):
        dt = datetime(2022, 9, 9, 17, 20, 0)
        self.assertEquals(self.instagrapiUtils.parseTakenAtTime(dt), [2022, 9, 9, 17, 20, 0])  # define the expected output by hand
        

    def test_parseMediaUrl(self):
        self.assertEquals(self.instagrapiUtils.parseMediaUrl(self.media.thumbnail_url), "www.google.com")  # define the expected output by hand

    def test_parseTakenAtLocation(self):
        self.assertEquals(self.instagrapiUtils.parseMediaUrl(self.media.location), []) # define the expected output by hand

    def test_getLocationPkCodeFromName(self):
        self.assertEqual(self.instagrapiUtils.getLocationPkCodeFromName("Farina del mio sacco"),1788391034730029)

    def test_getMostRecentMediasFromLocation(self):
        #maybe use a mock patch here
        self.assertEqual(type(self.instagrapiUtils.getMostRecentMediasFromLocation()), list[types.Media])

    def test_getMediaLocationCoordinates(self):
        self.assertEqual(self.instagrapiUtils.getMediaLocationCoordinates(self.media), {})

    def test_getMediaURL(self):
        self.assertEqual(self.instagrapiUtils.getMediaURL(self.media), "")

    def hasTaggedLocation(self):
        self.assertTrue(self.instagrapiUtils.hasTaggedLocation(self.media), True)



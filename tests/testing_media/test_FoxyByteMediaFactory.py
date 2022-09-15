import unittest
from unittest.mock import patch
import sys,os, datetime

from instagrapi import types


sys.path.insert(1, (str(sys.path[0]))+"/../../")
from crawler.media.FoxyByteMediaFactory import FoxyByteMediaFactory
from crawler.media.FoxyByteMedia import FoxyByteMedia



class TestFoxyByteMediaFactory(unittest.TestCase):
    def setUp(self):
        self.testFoxyByteMedia = FoxyByteMedia("CiDdJQjNSRP",
                                                1, 
                                                "william_lucchin", 
                                                [2022, 9, 3, 18, 5, 16],
                                                { "pk" : 3110887,
                                                "name" : "Ristorante Pizzeria Lunaelaltro - Marostica",
                                                "address" : "",
                                                "coordinates" : [11.660707634193, 45.736862428411],
                                                "category" : "Italian Restaurant",
                                                "phone" : "+390424478098",
                                                "website" : "http://www.lunaelaltro.it"},
                                                4,
                                                "",
                                                "https://instagram.fmxp5-1.fna.fbcdn.net/v/t39.30808-6/302560636_10225220452889775_4354789437307590688_n.jpg?stp=c0.64.1536.1920a_dst-jpg_e35_s1080x1080_sh0.08&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=103&_nc_ohc=pbzOsujR_swAX_Fq5nc&edm=AKmAybEAAAAA&ccb=7-5&ig_cache_key=MjkxOTMwNTE0OTExOTExNjczMQ%3D%3D.2-ccb7-5&oh=00_AT_CMVHHNQjkJyzNJLmCevqu9yU3bJHph5EDe7f0gYtK5g&oe=63239D11&_nc_sid=bcb968")
        
        self.testInstagrapiMedia = types.Media(pk='2919305163060880463', 
                                id='2919305163060880463_281443894', 
                                code='CiDdJQjNSRP', 
                                taken_at=datetime.datetime(2022, 9, 3, 18, 5, 16, tzinfo=datetime.timezone.utc), 
                                media_type=1, 
                                product_type='carousel_container', 
                                thumbnail_url= types.HttpUrl('https://instagram.fmxp5-1.fna.fbcdn.net/v/t39.30808-6/302560636_10225220452889775_4354789437307590688_n.jpg?stp=c0.64.1536.1920a_dst-jpg_e35_s1080x1080_sh0.08&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=103&_nc_ohc=pbzOsujR_swAX_Fq5nc&edm=AKmAybEAAAAA&ccb=7-5&ig_cache_key=MjkxOTMwNTE0OTExOTExNjczMQ%3D%3D.2-ccb7-5&oh=00_AT_CMVHHNQjkJyzNJLmCevqu9yU3bJHph5EDe7f0gYtK5g&oe=63239D11&_nc_sid=bcb968', 
                                                        scheme='https', 
                                                        host='instagram.fmxp5-1.fna.fbcdn.net', 
                                                        tld='net', 
                                                        host_type='domain', 
                                                        port='443', 
                                                        path='/v/t39.30808-6/302560636_10225220452889775_4354789437307590688_n.jpg', 
                                                        query='stp=c0.64.1536.1920a_dst-jpg_e35_s1080x1080_sh0.08&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=103&_nc_ohc=pbzOsujR_swAX_Fq5nc&edm=AKmAybEAAAAA&ccb=7-5&ig_cache_key=MjkxOTMwNTE0OTExOTExNjczMQ%3D%3D.2-ccb7-5&oh=00_AT_CMVHHNQjkJyzNJLmCevqu9yU3bJHph5EDe7f0gYtK5g&oe=63239D11&_nc_sid=bcb968'), 
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
                                                    profile_pic_url=types.HttpUrl('https://instagram.fmxp5-1.fna.fbcdn.net/v/t51.2885-19/220791469_538148194288015_175587587912182841_n.jpg?stp=dst-jpg_s150x150&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=107&_nc_ohc=N-9Qp0Nq5zkAX8jLkC7&edm=AKmAybEBAAAA&ccb=7-5&oh=00_AT-EZH5KaZ0dPby9NKaiSqPKArXsucUFLUuuNDIU5RI5Qg&oe=63229251&_nc_sid=bcb968', 
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
                                                        thumbnail_url=types.HttpUrl('https://instagram.fmxp5-1.fna.fbcdn.net/v/t39.30808-6/302560636_10225220452889775_4354789437307590688_n.jpg?stp=c0.64.1536.1920a_dst-jpg_e35_s1080x1080_sh0.08&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=103&_nc_ohc=pbzOsujR_swAX_Fq5nc&edm=AKmAybEAAAAA&ccb=7-5&ig_cache_key=MjkxOTMwNTE0OTExOTExNjczMQ%3D%3D.2-ccb7-5&oh=00_AT_CMVHHNQjkJyzNJLmCevqu9yU3bJHph5EDe7f0gYtK5g&oe=63239D11&_nc_sid=bcb968', 
                                                                            scheme='https', 
                                                                            host='instagram.fmxp5-1.fna.fbcdn.net', 
                                                                            tld='net', 
                                                                            host_type='domain', 
                                                                            port='443', 
                                                                            path='/v/t39.30808-6/302560636_10225220452889775_4354789437307590688_n.jpg', 
                                                                            query='stp=c0.64.1536.1920a_dst-jpg_e35_s1080x1080_sh0.08&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=103&_nc_ohc=pbzOsujR_swAX_Fq5nc&edm=AKmAybEAAAAA&ccb=7-5&ig_cache_key=MjkxOTMwNTE0OTExOTExNjczMQ%3D%3D.2-ccb7-5&oh=00_AT_CMVHHNQjkJyzNJLmCevqu9yU3bJHph5EDe7f0gYtK5g&oe=63239D11&_nc_sid=bcb968'), 
                                                                            media_type=1)],
                                clips_metadata={})

        self.testDBDictMedia = {'PostPartialURL' : "CiDdJQjNSRP",
                                'MediaType' : 1,
                                'AuthorUsername' : "william_lucchin", 
                                'TakenAtTime'    : [2022, 9, 3, 18, 5, 16],
                                'TakenAtLocation' : { "pk" : 3110887,
                                                        "Name" : "Ristorante Pizzeria Lunaelaltro - Marostica",
                                                        "Address" : "",
                                                        "Coordinates" : [11.660707634193, 45.736862428411],
                                                        "Category" : "Italian Restaurant",
                                                        "Phone" : "+390424478098",
                                                        "Website" : "http://www.lunaelaltro.it"},
                                "LikeCount": 4,
                                "CaptionText" : "",
                                "MediaURL" :"https://instagram.fmxp5-1.fna.fbcdn.net/v/t39.30808-6/302560636_10225220452889775_4354789437307590688_n.jpg?stp=c0.64.1536.1920a_dst-jpg_e35_s1080x1080_sh0.08&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=103&_nc_ohc=pbzOsujR_swAX_Fq5nc&edm=AKmAybEAAAAA&ccb=7-5&ig_cache_key=MjkxOTMwNTE0OTExOTExNjczMQ%3D%3D.2-ccb7-5&oh=00_AT_CMVHHNQjkJyzNJLmCevqu9yU3bJHph5EDe7f0gYtK5g&oe=63239D11&_nc_sid=bcb968"}

                                                
                                                


    def test_buildFromInstagrapiMediaAndLocation(self):
        self.assertEqual(FoxyByteMediaFactory.buildFromInstagrapiMediaAndLocation(self.testInstagrapiMedia, ["parsedTakenAt"], {1: "parsedlocation"}, "parsedurl"), self.testFoxyByteMedia) # TODO: pass params


    def test_buildFromDB(self):
        self.assertEqual(FoxyByteMediaFactory.buildFromDB(self.testDBDictMedia), self.testFoxyByteMedia)


unittest.main()
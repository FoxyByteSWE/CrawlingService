import unittest
from unittest.mock import patch
import sys,os, datetime

from instagrapi import types




sys.path.insert(1, (str(sys.path[0]))+"/../../crawler/media/")
sys.path.insert(1, (str(sys.path[0]))+"/../../crawler/")
from InstagrapiUtils import InstagrapiUtils
from FoxyByteMediaFactory import FoxyByteMediaFactory
from FoxyByteMedia import FoxyByteMedia



class TestFoxyByteMediaFactory(unittest.TestCase):
    def setUp(self):

        self.maxDiff = None
        
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
                                                    username='testuser', 
                                                    full_name='testuser', 
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
                                caption_text='testcaption', 
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
                                'AuthorUsername' : "testuser", 
                                'TakenAtTime'    : [2022, 9, 3, 18, 5, 16],
                                'TakenAtLocation' : { "pk" : 3110887,
                                                        "Name" : "Ristorante Pizzeria Lunaelaltro - Marostica",
                                                        "Address" : "",
                                                        "Coordinates" : [11.660707634193, 45.736862428411],
                                                        "Category" : "Italian Restaurant",
                                                        "Phone" : "+390424478098",
                                                        "Website" : "http://www.lunaelaltro.it"},
                                "LikeCount": 4,
                                "CaptionText" : "testcaption",
                                "MediaURLs" :"https://instagram.fmxp5-1.fna.fbcdn.net/v/t39.30808-6/302560636_10225220452889775_4354789437307590688_n.jpg?stp=c0.64.1536.1920a_dst-jpg_e35_s1080x1080_sh0.08&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=103&_nc_ohc=pbzOsujR_swAX_Fq5nc&edm=AKmAybEAAAAA&ccb=7-5&ig_cache_key=MjkxOTMwNTE0OTExOTExNjczMQ%3D%3D.2-ccb7-5&oh=00_AT_CMVHHNQjkJyzNJLmCevqu9yU3bJHph5EDe7f0gYtK5g&oe=63239D11&_nc_sid=bcb968"}



        self.testAlbumInstagrapiPost = types.Media(pk='2922888195445339045', id='2922888195445339045_244861834', code='CiQL1Pfs7Ol', taken_at=datetime.datetime(2022, 9, 8, 16, 44, 6, tzinfo=datetime.timezone.utc), media_type=8, product_type='carousel_container', thumbnail_url=None, location=None, user=types.UserShort(pk='244861834', username='marcouderzo', full_name='Marco Uderzo', profile_pic_url=types.HttpUrl('https://instagram.fmxp5-1.fna.fbcdn.net/v/t51.2885-19/300433054_476180640674958_6480412194885371836_n.jpg?stp=dst-jpg_s150x150&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=106&_nc_ohc=WdBRH6AOCNUAX8XlqQ4&edm=ABmJApABAAAA&ccb=7-5&oh=00_AT_P-AHIBMhXMG6fhKpjJla9sDn4QshOOXrE5tv0MVhAeg&oe=632EF626&_nc_sid=6136e7', scheme='https', host='instagram.fmxp5-1.fna.fbcdn.net', tld='net', host_type='domain', port='443', path='/v/t51.2885-19/300433054_476180640674958_6480412194885371836_n.jpg', query='stp=dst-jpg_s150x150&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=106&_nc_ohc=WdBRH6AOCNUAX8XlqQ4&edm=ABmJApABAAAA&ccb=7-5&oh=00_AT_P-AHIBMhXMG6fhKpjJla9sDn4QshOOXrE5tv0MVhAeg&oe=632EF626&_nc_sid=6136e7'), profile_pic_url_hd=None, is_private=False, stories=[]), comment_count=2, like_count=44, has_liked=False, caption_text='Asterix ⚔️\n\n#digitalart #art #artwork #artstation', accessibility_caption=None, usertags=[], video_url=None, view_count=0, video_duration=0.0, title='', resources=[types.Resource(pk='2922888190051368734', video_url=None, thumbnail_url=types.HttpUrl('https://instagram.fmxp5-1.fna.fbcdn.net/v/t51.2885-15/305581021_649382376752497_4108879936870536141_n.jpg?stp=dst-jpg_e35_p1080x1080&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=101&_nc_ohc=axKsxzOiApwAX-B_Tai&edm=ABmJApABAAAA&ccb=7-5&ig_cache_key=MjkyMjg4ODE5MDA1MTM2ODczNA%3D%3D.2-ccb7-5&oh=00_AT_ylOVVMjndmymijqPQWnraE-udOU14-fhqsZ5AQrtj3Q&oe=632E7DD8&_nc_sid=6136e7', scheme='https', host='instagram.fmxp5-1.fna.fbcdn.net', tld='net', host_type='domain', port='443', path='/v/t51.2885-15/305581021_649382376752497_4108879936870536141_n.jpg', query='stp=dst-jpg_e35_p1080x1080&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=101&_nc_ohc=axKsxzOiApwAX-B_Tai&edm=ABmJApABAAAA&ccb=7-5&ig_cache_key=MjkyMjg4ODE5MDA1MTM2ODczNA%3D%3D.2-ccb7-5&oh=00_AT_ylOVVMjndmymijqPQWnraE-udOU14-fhqsZ5AQrtj3Q&oe=632E7DD8&_nc_sid=6136e7'), media_type=1), types.Resource(pk='2922888190051309277', video_url=None, thumbnail_url=types.HttpUrl('https://instagram.fmxp5-1.fna.fbcdn.net/v/t51.2885-15/305891455_619332293079020_6104277027525319527_n.jpg?stp=dst-jpg_e35_p1080x1080&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=108&_nc_ohc=rqxlwvs4JOsAX9BD8-s&edm=ABmJApABAAAA&ccb=7-5&ig_cache_key=MjkyMjg4ODE5MDA1MTMwOTI3Nw%3D%3D.2-ccb7-5&oh=00_AT-jVLDcCr78o3ptPWduL9pUTdNAqgDklyoR8mxmBsxFHw&oe=632F09DE&_nc_sid=6136e7', scheme='https', host='instagram.fmxp5-1.fna.fbcdn.net', tld='net', host_type='domain', port='443', path='/v/t51.2885-15/305891455_619332293079020_6104277027525319527_n.jpg', query='stp=dst-jpg_e35_p1080x1080&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=108&_nc_ohc=rqxlwvs4JOsAX9BD8-s&edm=ABmJApABAAAA&ccb=7-5&ig_cache_key=MjkyMjg4ODE5MDA1MTMwOTI3Nw%3D%3D.2-ccb7-5&oh=00_AT-jVLDcCr78o3ptPWduL9pUTdNAqgDklyoR8mxmBsxFHw&oe=632F09DE&_nc_sid=6136e7'), media_type=1)], clips_metadata={})                                       


    def test_buildFromInstagrapiMediaAndLocation(self):
        media = FoxyByteMediaFactory.buildFromInstagrapiMediaAndLocation(self.testInstagrapiMedia, [2022, 9, 3, 18, 5, 16], { "pk" : 3110887,
                                                                                                                                        "Name" : "Ristorante Pizzeria Lunaelaltro - Marostica",
                                                                                                                                        "Address" : "",
                                                                                                                                        "Coordinates" : [11.660707634193, 45.736862428411],
                                                                                                                                        "Category" : "Italian Restaurant",
                                                                                                                                        "Phone" : "+390424478098",
                                                                                                                                        "Website" : "http://www.lunaelaltro.it"}, 
                                                                                                                                        "https://instagram.fmxp5-1.fna.fbcdn.net/v/t39.30808-6/302560636_10225220452889775_4354789437307590688_n.jpg?stp=c0.64.1536.1920a_dst-jpg_e35_s1080x1080_sh0.08&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=103&_nc_ohc=pbzOsujR_swAX_Fq5nc&edm=AKmAybEAAAAA&ccb=7-5&ig_cache_key=MjkxOTMwNTE0OTExOTExNjczMQ%3D%3D.2-ccb7-5&oh=00_AT_CMVHHNQjkJyzNJLmCevqu9yU3bJHph5EDe7f0gYtK5g&oe=63239D11&_nc_sid=bcb968") 
        self.assertEqual(media.getPostPartialURL(), "CiDdJQjNSRP")
        self.assertEqual(media.getMediaType(), 1)
        self.assertEqual(media.getAuthorUsername(), "testuser")
        self.assertEqual(media.getCaptionText(), "testcaption")
        self.assertEqual(media.getTakenAtTime(), [2022, 9, 3, 18, 5, 16])
        self.assertEqual(media.getTakenAtLocation(), { "pk" : 3110887,
                                                        "Name" : "Ristorante Pizzeria Lunaelaltro - Marostica",
                                                        "Address" : "",
                                                        "Coordinates" : [11.660707634193, 45.736862428411],
                                                        "Category" : "Italian Restaurant",
                                                        "Phone" : "+390424478098",
                                                        "Website" : "http://www.lunaelaltro.it"}),
                                                        
        self.assertEqual(media.getLikeCount(), 4)
        self.assertEqual(media.getMediaURLs(), "https://instagram.fmxp5-1.fna.fbcdn.net/v/t39.30808-6/302560636_10225220452889775_4354789437307590688_n.jpg?stp=c0.64.1536.1920a_dst-jpg_e35_s1080x1080_sh0.08&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=103&_nc_ohc=pbzOsujR_swAX_Fq5nc&edm=AKmAybEAAAAA&ccb=7-5&ig_cache_key=MjkxOTMwNTE0OTExOTExNjczMQ%3D%3D.2-ccb7-5&oh=00_AT_CMVHHNQjkJyzNJLmCevqu9yU3bJHph5EDe7f0gYtK5g&oe=63239D11&_nc_sid=bcb968")                                                                                                                                  




    def test_buildFromInstagrapiMediaAlbumAndLocation(self):
        urls= InstagrapiUtils.getMediaURL(InstagrapiUtils, self.testAlbumInstagrapiPost)
        print(urls)
        parsedurls = InstagrapiUtils.parseMediaUrl(InstagrapiUtils, urls) #FAILS: PARSEMEDIAURL SHOULD PARSE EVERY LINK BUT RETURN A LIST OF PARSED LINKS!
        print(urls)
        media = FoxyByteMediaFactory.buildFromInstagrapiMediaAndLocation(self.testAlbumInstagrapiPost, [2022, 9, 8, 16, 44, 6], {}, parsedurls) 
        self.assertEqual(media.getPostPartialURL(), "CiQL1Pfs7Ol")
        self.assertEqual(media.getMediaType(), 8)
        self.assertEqual(media.getAuthorUsername(), "marcouderzo")
        self.assertEqual(media.getCaptionText(), "Asterix ⚔️\n\n#digitalart #art #artwork #artstation")
        self.assertEqual(media.getTakenAtTime(), [2022, 9, 8, 16, 44, 6])
        self.assertEqual(media.getTakenAtLocation(), {}),                                                    
        self.assertEqual(media.getLikeCount(), 44)
        print("media urls are:")
        print(media.getMediaURLs())
        self.assertEqual(media.getMediaURLs(), ["https://instagram.fmxp5-1.fna.fbcdn.net/v/t51.2885-15/305581021_649382376752497_4108879936870536141_n.jpg?stp=dst-jpg_e35_p1080x1080&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=101&_nc_ohc=axKsxzOiApwAX-B_Tai&edm=ABmJApABAAAA&ccb=7-5&ig_cache_key=MjkyMjg4ODE5MDA1MTM2ODczNA%3D%3D.2-ccb7-5&oh=00_AT_ylOVVMjndmymijqPQWnraE-udOU14-fhqsZ5AQrtj3Q&oe=632E7DD8&_nc_sid=6136e7",
                                                "https://instagram.fmxp5-1.fna.fbcdn.net/v/t51.2885-15/305891455_619332293079020_6104277027525319527_n.jpg?stp=dst-jpg_e35_p1080x1080&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=108&_nc_ohc=rqxlwvs4JOsAX9BD8-s&edm=ABmJApABAAAA&ccb=7-5&ig_cache_key=MjkyMjg4ODE5MDA1MTMwOTI3Nw%3D%3D.2-ccb7-5&oh=00_AT-jVLDcCr78o3ptPWduL9pUTdNAqgDklyoR8mxmBsxFHw&oe=632F09DE&_nc_sid=6136e7"])                                                                                                                                  



    def test_buildFromDB(self):
        media = FoxyByteMediaFactory.buildFromDB(self.testDBDictMedia)
        self.assertEqual(media.getPostPartialURL(), "CiDdJQjNSRP")
        self.assertEqual(media.getMediaType(), 1)
        self.assertEqual(media.getAuthorUsername(), "testuser")
        self.assertEqual(media.getCaptionText(), "testcaption")
        self.assertEqual(media.getTakenAtTime(), [2022, 9, 3, 18, 5, 16])
        self.assertEqual(media.getTakenAtLocation(), { "pk" : 3110887,
                                                        "Name" : "Ristorante Pizzeria Lunaelaltro - Marostica",
                                                        "Address" : "",
                                                        "Coordinates" : [11.660707634193, 45.736862428411],
                                                        "Category" : "Italian Restaurant",
                                                        "Phone" : "+390424478098",
                                                        "Website" : "http://www.lunaelaltro.it"}),
                                                        
        self.assertEqual(media.getLikeCount(), 4)
        self.assertEqual(media.getMediaURLs(), "https://instagram.fmxp5-1.fna.fbcdn.net/v/t39.30808-6/302560636_10225220452889775_4354789437307590688_n.jpg?stp=c0.64.1536.1920a_dst-jpg_e35_s1080x1080_sh0.08&_nc_ht=instagram.fmxp5-1.fna.fbcdn.net&_nc_cat=103&_nc_ohc=pbzOsujR_swAX_Fq5nc&edm=AKmAybEAAAAA&ccb=7-5&ig_cache_key=MjkxOTMwNTE0OTExOTExNjczMQ%3D%3D.2-ccb7-5&oh=00_AT_CMVHHNQjkJyzNJLmCevqu9yU3bJHph5EDe7f0gYtK5g&oe=63239D11&_nc_sid=bcb968")                                                                                                                                   


unittest.main()
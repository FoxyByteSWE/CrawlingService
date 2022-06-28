import json
import sys
from pprint import pprint

class Restaurant:
	def __init__(self, pk = 0, medias = []):
		self.pk = pk
		self.medias = medias

class Media:
	def __init__(self, pk = 0, PostPartialURL = "", MediaType = 1, TakenAtTime = [], TakenAtLocation = {}, LikeCount = 0, CaptionText = "", MediaURL = ""):
		self.pk = pk
		self.PostPartialURL = PostPartialURL
		self.MediaType = MediaType
		self.TakenAtTime = TakenAtTime
		self.TakenAtLocation = TakenAtLocation
		self.LikeCount = LikeCount
		self.CaptionText = CaptionText
		self.MediaURL = MediaURL

def json2Restaurants(path):

	with open(path, 'r') as inputfile:
		data = json.load(inputfile)

	restaurant_list = []

	for restaurant in data:
		media_list = []

		for media in data[restaurant]:
			m = Media(media["TakenAtLocation"]["pk"], media["PostPartialURL"], media["MediaType"], media["TakenAtTime"], media["TakenAtLocation"], media["LikeCount"], media["CaptionText"], media["MediaURL"])
			media_list.append(m)

		restaurant_list.append(Restaurant(restaurant, media_list))

	return restaurant_list

#def Media2json(medias):
	#out = '{"'
	#for m in medias:
		#out += json.dumps(m.__dict__)
	#return out

def main():
	restaurants = json2Restaurants((str(sys.path[0]))+"/data/locationsData.json")
	for r in restaurants:
		print(r.pk)
		for m in r.medias:
			pprint(vars(m))

if __name__ == "__main__":
	main()

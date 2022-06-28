import json
import sys
from pprint import pprint

class Restaurant:
	def __init__(self, pk = 0, medias = []):
		self.pk = pk
		self.medias = medias

class Media:
	def __init__(self, PostPartialURL = "", MediaType = 1, TakenAtTime = [], TakenAtLocation = {}, LikeCount = 0, CaptionText = "", MediaURL = ""):
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
			m = Media(media["PostPartialURL"], media["MediaType"], media["TakenAtTime"], media["TakenAtLocation"], media["LikeCount"], media["CaptionText"], media["MediaURL"])
			media_list.append(m)

		restaurant_list.append(Restaurant(restaurant, media_list))

	return restaurant_list

def Restaurants2json(restaurants, file):
	out = '{'
	for r in restaurants:
		out += '"' + r.pk + '": '
		for m in r.medias:
			out += '['
			out += json.dumps(m.__dict__)
			out += ']'
	out += '}'
	f = open(file, "w")
	f.write(out)
	f.close()

def main():
	restaurants = json2Restaurants((str(sys.path[0]))+"/data/locationsData.json")
	for r in restaurants:
		print(r.pk)
		for m in r.medias:
			pprint(vars(m))
	Restaurants2json(restaurants, "test.json")

if __name__ == "__main__":
	main()

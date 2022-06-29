import json
import sys
import datetime
from pprint import pprint
	
class Restaurant:
	def __init__(self, pk = 0, medias = []):
		self.pk = pk
		self.medias = medias

	def isOld(self, m):
		now = datetime.datetime.now()
		post_taken_at = datetime.datetime(m.TakenAtTime[0], m.TakenAtTime[1], m.TakenAtTime[2], m.TakenAtTime[3], m.TakenAtTime[4], m.TakenAtTime[5])
		age = (now - post_taken_at).days
		if age > 720:
			return True
		else:
			return False
	
	def removeOldMedias(self):
		self.medias = [m for m in self.medias if not self.isOld(m)]
		
	#def toJSON(self):
		#return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
				

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
	out = ""
	for r in restaurants:
		out += '{'
		out += '"' + r.pk + '": '
		for m in r.medias:
			out += '['
			out += json.dumps(m.__dict__)
			out += '], '
		out = out[:-2]
		out += '}'
		out += '\n'

	out = out[:-1]
	f = open(file, "w")
	f.write(out)
	f.close()


def removeOldMedias(restaurants):
	for r in restaurants:
		r.removeOldMedias()

def main():
	restaurants = json2Restaurants((str(sys.path[0]))+"/data/locationsData.json")
	for r in restaurants:
		print(r.pk)
		for m in r.medias:
			pprint(vars(m))
	Restaurants2json(restaurants, "test.json")
	removeOldMedias(restaurants)
	for r in restaurants:
		print(r.pk)
		for m in r.medias:
			pprint(vars(m))

if __name__ == "__main__":
	main()

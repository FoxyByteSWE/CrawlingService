import json
import sys
import datetime
from pprint import pprint
	
class Restaurant:
	def __init__(self, pk = 0, medias = [], name = "", category = "", address = "", website = "", phone = "", coordinates = "", ranking = -1):
		self.pk = pk
		self.medias = medias
		self.name = name
		self.category = category
		self.address = address
		self.website = website
		self.phone = phone
		self.coordinates = coordinates
		self.ranking = ranking

	def assignValues(self):
		for m in self.medias:
			if self.name == "" and m.TakenAtLocation["name"] != "":
				self.name = m.TakenAtLocation["name"]
			if self.category == "" and m.TakenAtLocation["category"] != "":
				self.category = m.TakenAtLocation["category"]
			if self.address == "" and m.TakenAtLocation["address"] != "":
				self.address = m.TakenAtLocation["address"]
			if self.website == "" and m.TakenAtLocation["website"] != "":
				self.website = m.TakenAtLocation["website"]
			if self.phone == "" and m.TakenAtLocation["phone"] != "":
				self.phone = m.TakenAtLocation["phone"]
			if self.coordinates == "" and m.TakenAtLocation["coordinates"] != "":
				self.coordinates = m.TakenAtLocation["coordinates"]

	def returnFormattedRanking(self):
		return '{0:.1f}'.format(self.ranking)

	def printFormattedRanking(self):
		print('{0:.1f}'.format(self.ranking))

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
	out = '{'
	for r in restaurants:
		out += '"' + r.pk + '": ['
		for m in r.medias:
			out += json.dumps(m.__dict__)
			out += ', '
		out = out[:-2]
		out += '], '

	out = out[:-2]
	out += '}'
	f = open(file, "w")
	f.write(out)
	f.close()


def removeOldMedias(restaurants):
	for r in restaurants:
		r.removeOldMedias()

def main():
	restaurants = json2Restaurants((str(sys.path[0]))+"/data/locationsData.json")
	for r in restaurants:
		r.assignValues()

	for r in restaurants:
		pprint(vars(r))
		for m in r.medias:
			pprint(vars(m))

	Restaurants2json(restaurants, (str(sys.path[0]))+"/data/test_Restaurants2json.json")

	removeOldMedias(restaurants)

	for r in restaurants:
		pprint(vars(r))
		for m in r.medias:
			pprint(vars(m))

if __name__ == "__main__":
	main()

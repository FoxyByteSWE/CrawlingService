import json
import sys
from pprint import pprint

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
	#def buildFromJSON(file):
		#self = json.loads(file, object_hook=lambda d: SimpleNamespace(**d)k0)

def json2Media(path):
	list = []
	with open(path, 'r') as inputfile:
		data = json.load(inputfile)
	for i in data:
		for j in data[i]:
			m = Media(j["TakenAtLocation"]["pk"], j["PostPartialURL"], j["MediaType"], j["TakenAtTime"], j["TakenAtLocation"], j["LikeCount"], j["CaptionText"], j["MediaURL"])
			list.append(m)
	return list

#def Media2json(medias):
	#out = '{"'
	#for m in medias:
		#out += json.dumps(m.__dict__)
	#return out

def main():
	medias = json2Media((str(sys.path[0]))+"/data/locationsData.json")
	for m in medias:
		pprint(vars(m))
	#print(Media2json(medias))

if __name__ == "__main__":
	main()

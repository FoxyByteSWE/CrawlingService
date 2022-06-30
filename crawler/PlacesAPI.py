from pprint import pprint
import os, json, sys
import googlemaps # pip install googlemaps
import requests

API_KEY = open('API_KEY.txt').read()
map_client = googlemaps.Client(API_KEY)

def getAllLocationsFromJSON():
	filepath = (str(sys.path[0]))+"/data/locations.json"
	with open(filepath) as locations:
		try:
			data = json.load(locations)
			return data
		except Exception as e:
			print(e)
			return None


def get_place_info(location_name):
    try:
        # location_name = 'Pizzeria Lunaelaltro'
        response = map_client.places(query=location_name)
        results = response.get('results')[0]
        return results
    except Exception as e:
        print(e)
        return None



def main():
    locations = getAllLocationsFromJSON()
    locname = locations["4706333"].get("name")
    coords = locations["4706333"].get("coordinates")
    print(locname)
    fromGPlaces= get_place_info(locname)
    # locationbias, Point: A single lat/lng coordinate. Use the following format: point:lat,lng.

    #directly from API documentation

    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=Museum%20of%20Contemporary%20Art%20Australia&inputtype=textquery&fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&key=YOUR_API_KEY"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)



if __name__ == "__main__":
    main()
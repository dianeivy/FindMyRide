import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key=tmp_key)

geocode_result = gmaps.geocode('Cambridge, MA')


starting_lat = geocode_result[0]['geometry']['location']['lat']
starting_lon = geocode_result[0]['geometry']['location']['lng']

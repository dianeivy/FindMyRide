import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyDHyED6bTDCiE5ixR3hzkeyONB132AO64s')

geocode_result = gmaps.geocode('227 Charles Street, Cambridge, MA')


starting_lat = geocode_result[0]['geometry']['location']['lat']
starting_lon = geocode_result[0]['geometry']['location']['lng']
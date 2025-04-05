import requests
import urllib.parse

geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
loc1 = "Washington, D.C."
loc2 = "Baltimore, Maryland"
key = "25aef206-f4bb-47b7-86ef-62c500dea387"  # Replace with your API key
url = geocode_url + urllib.parse.urlencode({"q": loc1, "limit": "1", "key": key})

replydata = requests.get(url)
json_data = replydata.json()
json_status = replydata.status_code

json_status = replydata.status_code
if json_status == 200:
    print("Geocoding API URL for " + loc1 + ".\n" + url)

def geocoding(location, key):
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    print("Geocoding API URL for " + location + ".\n" + url)
    if json_status == 200:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
    else:
        lat = "null"
        lng = "null"
    return json_status, lat, lng

orig = geocoding(loc1, key)
print(orig)
dest = geocoding(loc2, key)
print(dest)

if json_status == 200:
    name = json_data["hits"][0]["name"]
    value = json_data["hits"][0]["osm_value"]
    if "country" in json_data["hits"][0]:
        country = json_data["hits"][0]["country"]
    else:
        country = ""
    if "state" in json_data["hits"][0]:
        state = json_data["hits"][0]["state"]
    else:
        state = ""
    if len(state) != 0 and len(country) != 0:
        new_loc = name + ", " + state + ", " + country
    elif len(state) != 0:
        new_loc = name + ", " + country
    else:
        new_loc = name
    print("Geocoding API URL for " + new_loc + " (Location Type: " + value + ")\n" + url)

    
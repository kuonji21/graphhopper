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
print(json_data)
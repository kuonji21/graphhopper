import requests
import urllib.parse

# Graphhopper API URLs
geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"

# API Key (replace with your key)
key = "25aef206-f4bb-47b7-86ef-62c500dea387"

# Function to get geocoding data
def geocoding(location, key):
    while location == "":
        location = input("Enter the location again: ")
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")
        if state and country:
            new_loc = f"{name}, {state}, {country}"
        elif country:
            new_loc = f"{name}, {country}"
        else:
            new_loc = name
        print(f"Geocoding API URL for {new_loc} (Location Type: {value})\n{url}")
        return json_status, lat, lng, new_loc
    else:
        print(f"Geocode API status: {json_status}\nError message: {json_data.get('message', 'No results found')}")
        return json_status, "null", "null", location

# Main application loop
while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Vehicle profiles available on Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car, bike, foot")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    vehicle = input("Enter a vehicle profile from the list above: ")
    if vehicle == "quit" or vehicle == "q":
        break
    elif vehicle not in ["car", "bike", "foot"]:
        vehicle = "car"
        print("No valid vehicle profile was entered. Using the car profile.")

    loc1 = input("Starting Location: ")
    if loc1 == "quit" or loc1 == "q":
        break
    orig = geocoding(loc1, key)

    loc2 = input("Destination: ")
    if loc2 == "quit" or loc2 == "q":
        break
    dest = geocoding(loc2, key)

    if orig[0] == 200 and dest[0] == 200:
        op = f"&point={orig[1]}%2C{orig[2]}"
        dp = f"&point={dest[1]}%2C{dest[2]}"
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()

        print("\n=================================================")
        print(f"Directions from {orig[3]} to {dest[3]} by {vehicle}")
        print("=================================================")

        if paths_status == 200:
            miles = (paths_data["paths"][0]["distance"]) / 1000 / 1.61
            km = (paths_data["paths"][0]["distance"]) / 1000
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            print(f"Distance Traveled: {miles:.1f} miles / {km:.1f} km")
            print(f"Trip Duration: {hr:02d}:{min:02d}:{sec:02d}")
            print("=================================================")

            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                print(f"{path} ({distance / 1000:.1f} km / {distance / 1000 / 1.61:.1f} miles)")
            print("=================================================")
        else:
            print(f"Routing API Status: {paths_status}\nError message: {paths_data.get('message', 'No route found')}")
import requests
import urllib.parse
import time

"""
Graphhopper Route Planner Enhancement
Team: Montemar Squad
Members:
- John Ken Ompad - Enhanced UI with Menu System
- Jomari G. Tero - Favorite Locations
- Niño Angelo A. Lawan - Simple Route Visualization
- Lance Montemar - Simple Export Directions

This application uses the Graphhopper API to find routes between locations,
with enhanced features added by our team.
"""


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


# Feature 1: Enhanced UI - Clear screen function (John Ken Ompad)
def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

# Feature 1: Enhanced UI - Display header (John Ken Ompad)
def display_header(title="Graphhopper Route Planner"):
    """Display a header with the given title"""
    clear_screen()
    print("=" * 50)
    print(f"{title:^50}")
    print("=" * 50)

# Feature 1: Enhanced UI - Main menu function (John Ken Ompad)
def display_menu():
    """Display the main menu and get user choice"""
    display_header()
    print("\n1. Find route between locations")
    print("2. Manage favorite locations")
    print("3. About this application")
    print("4. Exit")
    print("\nEnter 'q' or 'quit' at any prompt to return to this menu.")
    choice = input("\nEnter your choice (1-4): ")
    return choice

def about():
    """Display information about the application"""
    display_header("About This Application")
    
    print("\nGraphhopper Route Planner")
    print("Team: Montemar Squad")
    print("\nMembers:")
    print("- John Ken Ompad - Enhanced UI with Menu System")
    print("- Jomari G. Tero - Favorite Locations")
    print("- Niño Angelo A. Lawan - Simple Route Visualization")
    print("- Lance Montemar - Simple Export Directions")
    
    print("\nThis application uses the Graphhopper API to find routes between")
    print("locations with enhanced features added by our team.")
    
    input("\nPress Enter to continue...")

def main():
    """Main application function"""
    while True:
        choice = display_menu()
        
        if choice == "1":
            find_route()
        elif choice == "2":
            manage_favorites()
        elif choice == "3":
            about()
        elif choice == "4" or choice.lower() in ["q", "quit"]:
            print("\nThank you for using Graphhopper Route Planner!")
            break
        else:
            print("Invalid choice. Please try again.")
            time.sleep(1)

# Update the find_route function to use the enhanced UI
def find_route():
    """Find a route between two locations"""
    display_header("Find Route")
    
    # Rest of the function remains the same
    # ...
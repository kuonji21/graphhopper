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

import requests
import urllib.parse
import os
import webbrowser
import time

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
        value = json_data["hits"][0].get("osm_value", "unknown")
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

# Feature 2: Favorite Locations - Save and load favorites (Jomari G. Tero)
def save_favorite(name, location_data):
    """
    Save a location to favorites.txt
    
    Parameters:
    name -- Name to save the location under
    location_data -- Location data tuple (status, lat, lng, name)
    """
    try:
        with open("favorites.txt", "a") as f:
            f.write(f"{name}|{location_data[1]}|{location_data[2]}|{location_data[3]}\n")
        print(f"Location '{name}' saved to favorites.")
    except Exception as e:
        print(f"Error saving favorite: {e}")

def load_favorites():
    """
    Load all saved favorite locations
    
    Returns:
    dict -- Dictionary of favorite locations or empty dict if none found
    """
    favorites = {}
    if os.path.exists("favorites.txt"):
        try:
            with open("favorites.txt", "r") as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split("|")
                        if len(parts) == 4:
                            name, lat, lng, loc_name = parts
                            favorites[name] = (200, lat, lng, loc_name)
        except Exception as e:
            print(f"Error loading favorites: {e}")
    return favorites

def display_favorites():
    """Display all saved favorite locations"""
    favorites = load_favorites()
    if not favorites:
        print("No favorite locations saved.")
        return False
    
    print("\n--- Favorite Locations ---")
    for name, data in favorites.items():
        print(f"{name}: {data[3]}")
    print("-------------------------")
    return True

def use_favorite(name):
    """Use a favorite location"""
    favorites = load_favorites()
    if name in favorites:
        return favorites[name]
    else:
        print(f"Favorite '{name}' not found.")
        return None

# Feature 3: Simple Route Visualization (Niño Angelo A. Lawan)
def visualize_route(orig, dest):
    """
    Open a map in the browser showing the route between two points
    
    Parameters:
    orig -- Origin location data (status, lat, lng, name)
    dest -- Destination location data (status, lat, lng, name)
    """
    # Create a Google Maps URL for the route
    maps_url = f"https://www.google.com/maps/dir/?api=1&origin={orig[1]},{orig[2]}&destination={dest[1]},{dest[2]}&travelmode=driving"
    
    print(f"\nOpening route map in your browser...")
    webbrowser.open(maps_url)
    print("If the browser doesn't open automatically, use this URL:")
    print(maps_url)

# Feature 4: Simple Export Directions (Lance Montemar)
def export_directions(orig, dest, vehicle, paths_data):
    """
    Export directions to a simple text file
    
    Parameters:
    orig -- Origin location data
    dest -- Destination location data
    vehicle -- Vehicle profile used
    paths_data -- Route data from Graphhopper API
    """
    try:
        # Create a simple filename
        filename = f"directions_{orig[3]}_to_{dest[3]}.txt"
        # Replace characters that might cause issues in filenames
        filename = filename.replace(" ", "_").replace(",", "").replace("/", "_")
        
        with open(filename, "w") as f:
            f.write("=================================================\n")
            f.write(f"Directions from {orig[3]} to {dest[3]} by {vehicle}\n")
            f.write("=================================================\n")
            
            miles = (paths_data["paths"][0]["distance"]) / 1000 / 1.61
            km = (paths_data["paths"][0]["distance"]) / 1000
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            
            f.write(f"Distance Traveled: {miles:.1f} miles / {km:.1f} km\n")
            f.write(f"Trip Duration: {hr:02d}:{min:02d}:{sec:02d}\n")
            f.write("=================================================\n")
            
            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                f.write(f"{path} ({distance / 1000:.1f} km / {distance / 1000 / 1.61:.1f} miles)\n")
            
            f.write("=================================================\n")
        
        print(f"\nDirections exported to {filename}")
    except Exception as e:
        print(f"Error exporting directions: {e}")

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

def find_route():
    """Find a route between two locations"""
    display_header("Find Route")
    
    print("Vehicle profiles available on Graphhopper:")
    print("car, bike, foot")
    vehicle = input("\nEnter a vehicle profile from the list above: ")
    if vehicle in ["quit", "q"]:
        return
    elif vehicle not in ["car", "bike", "foot"]:
        vehicle = "car"
        print("No valid vehicle profile was entered. Using the car profile.")

    # Get starting location
    print("\nYou can use a saved favorite by typing 'fav:name'")
    loc1 = input("Starting Location: ")
    if loc1 in ["quit", "q"]:
        return
    
    # Check if it's a favorite
    if loc1.startswith("fav:"):
        fav_name = loc1[4:].strip()
        orig = use_favorite(fav_name)
        if not orig:
            orig = geocoding(input("Enter the starting location: "), key)
    else:
        orig = geocoding(loc1, key)

    # Get destination
    print("\nYou can use a saved favorite by typing 'fav:name'")
    loc2 = input("Destination: ")
    if loc2 in ["quit", "q"]:
        return
    
    # Check if it's a favorite
    if loc2.startswith("fav:"):
        fav_name = loc2[4:].strip()
        dest = use_favorite(fav_name)
        if not dest:
            dest = geocoding(input("Enter the destination: "), key)
    else:
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
            
            # After displaying route, offer options
            print("\nOptions:")
            print("1. Save origin to favorites")
            print("2. Save destination to favorites")
            print("3. View route on map")
            print("4. Export directions to file")
            print("5. Return to main menu")
            
            option = input("\nEnter option (1-5): ")
            if option == "1":
                name = input("Enter name for this favorite: ")
                save_favorite(name, orig)
            elif option == "2":
                name = input("Enter name for this favorite: ")
                save_favorite(name, dest)
            elif option == "3":
                visualize_route(orig, dest)
            elif option == "4":
                export_directions(orig, dest, vehicle, paths_data)
        else:
            print(f"Routing API Status: {paths_status}\nError message: {paths_data.get('message', 'No route found')}")
    
    input("\nPress Enter to continue...")

def manage_favorites():
    """Manage favorite locations"""
    display_header("Manage Favorites")
    
    if not display_favorites():
        print("No favorites found.")
    
    print("\nOptions:")
    print("1. Add new favorite")
    print("2. Return to main menu")
    
    option = input("\nEnter option (1-2): ")
    if option == "1":
        name = input("Enter name for this favorite: ")
        location = input("Enter location: ")
        loc_data = geocoding(location, key)
        if loc_data[0] == 200:
            save_favorite(name, loc_data)
    
    input("\nPress Enter to continue...")

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

# Run the application
if __name__ == "__main__":
    main()

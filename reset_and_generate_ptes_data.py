import random
from pymongo import MongoClient, ASCENDING
from faker import Faker
import logging
from decimal import Decimal

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
MONGO_URI = "mongodb+srv://<username>:<password>@<your-cluster-url>/ptes?retryWrites=true&w=majority"
DATABASE_NAME = "ptes"
NUMBER_OF_LOCATIONS = 100
NUMBER_OF_TRANSPORT_MODES = 9  # As per PTES
NUMBER_OF_ROUTES = 500
NUMBER_OF_JOURNEYS = 1000

# Bounding Box for Coordinates (Hong Kong Approximate)
MIN_LONGITUDE = 113.8
MAX_LONGITUDE = 114.4
MIN_LATITUDE = 22.25
MAX_LATITUDE = 22.55

# Sample Categories
CATEGORIES = [
    "Park",
    "Restaurant",
    "Museum",
    "Cafe",
    "Library",
    "Theater",
    "Store",
    "Hotel",
    "Gym",
    "Bar"
]

# Initialize Faker
fake = Faker()

def generate_random_coordinates():
    """Generate random coordinates within the specified bounding box."""
    longitude = float(random.uniform(MIN_LONGITUDE, MAX_LONGITUDE))
    latitude = float(random.uniform(MIN_LATITUDE, MAX_LATITUDE))
    return [longitude, latitude]

def convert_decimals(obj):
    """Recursively convert Decimal instances to float."""
    if isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimals(item) for item in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj

def reset_collections(db):
    """Drop existing collections to reset the database."""
    collections = ['locations', 'transport_modes', 'routes', 'stops', 'journeys']
    for col in collections:
        if col in db.list_collection_names():
            db.drop_collection(col)
            logger.info(f"Dropped collection: {col}")
    logger.info("All specified collections have been reset.")

def create_geospatial_index(db):
    """Create a 2dsphere index on the 'location' field in 'locations' collection."""
    db.locations.create_index([("location", "2dsphere")])
    logger.info("Created geospatial index on 'location' field in 'locations' collection.")

def generate_transport_modes(db):
    """Insert predefined transport modes into the 'transport_modes' collection."""
    transport_modes = [
        {"mode_id": "MTR", "name": "Mass Transit Railway", "description": "Hong Kong's rapid transit railway system."},
        {"mode_id": "LRT", "name": "Light Rail Transit", "description": "Light rail system in Hong Kong."},
        {"mode_id": "Bus", "name": "Franchised Bus", "description": "Standard franchised bus services."},
        {"mode_id": "GreenMinibus", "name": "Green Minibus", "description": "Small-capacity bus services."},
        {"mode_id": "Tram", "name": "Tram", "description": "Historic tram services on Hong Kong Island."},
        {"mode_id": "PeakTram", "name": "Peak Tram", "description": "Cable funicular railway."},
        {"mode_id": "Ferry", "name": "Ferry", "description": "Maritime ferry services."},
        {"mode_id": "Coach", "name": "Cross Boundary Coach", "description": "Coaches to Lok Ma Chau/Huanggang."},
        {"mode_id": "BusToMaWan", "name": "Bus to Ma Wan and Discovery Bay", "description": "Bus services to specific districts."}
    ]
    db.transport_modes.insert_many(transport_modes)
    logger.info(f"Inserted {len(transport_modes)} transport modes.")

def generate_locations(db):
    """Generate and insert random locations into the 'locations' collection."""
    locations = []
    for _ in range(NUMBER_OF_LOCATIONS):
        location = {
            "name": fake.street_name(),
            "type": random.choice(["Boarding", "Alighting", "Interchange"]),
            "location": {
                "type": "Point",
                "coordinates": generate_random_coordinates()
            },
            "address": fake.address(),
            "category": random.choice(["Residential", "Commercial", "Park", "Terminal", "Station"])
        }
        locations.append(location)
    # Convert any Decimal instances to float
    locations_to_insert = [convert_decimals(loc) for loc in locations]
    inserted_locations = db.locations.insert_many(locations_to_insert)
    logger.info(f"Inserted {len(inserted_locations.inserted_ids)} locations.")
    return inserted_locations.inserted_ids

def generate_routes(db):
    """Generate and insert random routes into the 'routes' collection."""
    transport_modes = list(db.transport_modes.find())
    locations = list(db.locations.find())
    routes = []
    for i in range(NUMBER_OF_ROUTES):
        mode = random.choice(transport_modes)
        start_location = random.choice(locations)
        end_location = random.choice(locations)
        
        fare = round(random.uniform(5.0, 100.0), 2)
        estimated_time = random.randint(15, 120)  # in minutes
        service_type = random.choice(["Express", "Regular"])
        timetable = {
            "start_time": f"{random.randint(4, 6)}:{random.randint(0,59):02d}",
            "end_time": f"{random.randint(22, 23)}:{random.randint(0,59):02d}",
            "frequency": f"{random.randint(1,10)} mins"
        }
        route_number = f"{mode['mode_id']}-{random.randint(100,999)}"
        
        route = {
            "route_number": route_number,
            "mode_id": mode["mode_id"],
            "start_location_id": start_location["_id"],
            "end_location_id": end_location["_id"],
            "stops": [],  # To be populated later
            "fare": fare,
            "estimated_time": estimated_time,
            "service_type": service_type,
            "timetable": timetable
        }
        routes.append(route)
        
        if (i + 1) % 100 == 0:
            logger.info(f"Prepared {i + 1} routes.")
    
    # Convert Decimals to float
    routes_to_insert = [convert_decimals(route) for route in routes]
    inserted_routes = db.routes.insert_many(routes_to_insert)
    logger.info(f"Inserted {len(inserted_routes.inserted_ids)} routes.")
    return inserted_routes.inserted_ids

def generate_stops(db, route_ids):
    """Generate and insert random stops for each route into the 'stops' collection."""
    routes = list(db.routes.find({"_id": {"$in": route_ids}}))
    locations = list(db.locations.find())
    stops = []
    for route in routes:
        num_stops = random.randint(5, 20)
        route_stops = random.sample(locations, num_stops)
        for seq, stop in enumerate(route_stops, start=1):
            arrival_hour = random.randint(5, 23)
            arrival_minute = random.randint(0, 59)
            departure_hour = random.randint(5, 23)
            departure_minute = random.randint(0, 59)
            stop_doc = {
                "route_id": route["_id"],
                "stop_sequence": seq,
                "location_id": stop["_id"],
                "arrival_time": f"{arrival_hour}:{arrival_minute:02d}",
                "departure_time": f"{departure_hour}:{departure_minute:02d}"
            }
            stops.append(stop_doc)
            # Update route's stops list
            route["stops"].append(stop["_id"])
        if (route_ids.index(route["_id"]) + 1) % 100 == 0:
            logger.info(f"Prepared stops for {route_ids.index(route['_id']) + 1} routes.")
    
    # Insert all stops
    stops_to_insert = [convert_decimals(stop) for stop in stops]
    inserted_stops = db.stops.insert_many(stops_to_insert)
    logger.info(f"Inserted {len(inserted_stops.inserted_ids)} stops.")
    
    # Update routes with stop references
    for route in routes:
        db.routes.update_one(
            {"_id": route["_id"]},
            {"$set": {"stops": route["stops"]}}
        )
    logger.info("Updated routes with stop references.")
    return inserted_stops.inserted_ids

def generate_journeys(db):
    """Generate and insert random journeys into the 'journeys' collection."""
    locations = list(db.locations.find())
    routes = list(db.routes.find())
    stops = list(db.stops.find())
    
    journeys = []
    for _ in range(NUMBER_OF_JOURNEYS):
        origin = random.choice(locations)
        destination = random.choice(locations)
        
        if origin["_id"] == destination["_id"]:
            continue  # Skip same origin and destination
        
        # Find routes that start from origin and end at destination
        possible_routes = [route for route in routes if route["start_location_id"] == origin["_id"] and route["end_location_id"] == destination["_id"]]
        
        if not possible_routes:
            continue  # No direct route available
        
        selected_route = random.choice(possible_routes)
        
        # Find stops for the selected route
        route_stops = [stop for stop in stops if stop["route_id"] == selected_route["_id"]]
        
        if not route_stops:
            continue  # No stops available for this route
        
        boarding_stop = random.choice(route_stops)["location_id"]
        alighting_stop = random.choice(route_stops)["location_id"]
        
        journey = {
            "origin_id": origin["_id"],
            "destination_id": destination["_id"],
            "routes": [
                {
                    "route_id": selected_route["_id"],
                    "mode_id": selected_route["mode_id"],
                    "boarding_stop_id": boarding_stop,
                    "alighting_stop_id": alighting_stop,
                    "fare": selected_route["fare"],
                    "estimated_time": selected_route["estimated_time"],
                    "interchanges": 0
                }
            ],
            "total_fare": selected_route["fare"],
            "total_time": selected_route["estimated_time"],
            "number_of_interchanges": 0
        }
        journeys.append(journey)
    
    # Convert Decimals to float
    journeys_to_insert = [convert_decimals(journey) for journey in journeys]
    if journeys_to_insert:
        inserted_journeys = db.journeys.insert_many(journeys_to_insert)
        logger.info(f"Inserted {len(inserted_journeys.inserted_ids)} journeys.")
    else:
        logger.warning("No journeys were inserted.")
    
def main():
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        logger.info(f"Connected to MongoDB Atlas database: {DATABASE_NAME}")
        
        # Reset collections
        reset_collections(db)
        
        # Create geospatial index
        create_geospatial_index(db)
        
        # Generate and insert transport modes
        generate_transport_modes(db)
        
        # Generate and insert locations
        location_ids = generate_locations(db)
        
        # Generate and insert routes
        route_ids = generate_routes(db)
        
        # Generate and insert stops
        stop_ids = generate_stops(db, route_ids)
        
        # Generate and insert journeys
        generate_journeys(db)
        
        logger.info("Reset and data generation completed successfully.")
    
    except Exception as e:
        logger.error("An error occurred during the reset and data generation process:", exc_info=True)

if __name__ == "__main__":
    main()

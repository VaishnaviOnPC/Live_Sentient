# geo_utils.py

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time


geolocator = Nominatim(user_agent="live_sentient_app")


def resolve_location(location: str, retries: int = 3) -> dict:
    """
    Resolve a location string to geographic coordinates.

    Args:
        location (str): Freeform location input (e.g., "San Francisco, CA").
        retries (int): Number of retry attempts in case of timeout.

    Returns:
        dict: {latitude, longitude, display_name} or error message
    """
    for attempt in range(retries):
        try:
            geo = geolocator.geocode(location)
            if geo:
                return {
                    "latitude": geo.latitude,
                    "longitude": geo.longitude,
                    "display_name": geo.address
                }
            else:
                return {"error": "Location not found."}
        except GeocoderTimedOut:
            time.sleep(1)
    return {"error": "Geocoding service timeout."}

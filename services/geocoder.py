from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable, GeocoderTimedOut

geolocator = Nominatim(
    user_agent="crisisgrid_app",
    timeout=10
)

def get_coordinates(city):
    try:
        location = geolocator.geocode(city)

        if location:
            return (
                location.latitude,
                location.longitude
            )

        return None

    except (GeocoderUnavailable, GeocoderTimedOut):
        return None

    except Exception:
        return None
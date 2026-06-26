CITY_COORDINATES = {
    "mumbai": (19.0760, 72.8777),
    "pune": (18.5204, 73.8567),
    "delhi": (28.6139, 77.2090),
}

def get_coordinates(city):
    if not city:
        return None

    return CITY_COORDINATES.get(city.lower().strip())
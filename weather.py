import requests

def get_location_coords(location):
    """Returns location coordinates and metadata"""
    response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": location, "count": 1}
    ).json()
    
    if "results" not in response:
        return None
    
    result = response["results"][0]
    return {
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "country": result["country"],
        "city": result["name"]
    }

def get_weather(latitude, longitude):
    """Gets weather data in 12-hour intervals"""
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "temperature_2m,relative_humidity_2m",
            "timezone": "GMT"
        }
    ).json()
    
    data = response["hourly"]
    # Return data points every 12 hours
    return [(
        data["temperature_2m"][i],
        data["relative_humidity_2m"][i],
        data["time"][i]
    ) for i in range(0, len(data["time"]), 12)]

if __name__ == "__main__":
    # Example usage for testing
    location = get_location_coords("osaka")
    if location:
        weather = get_weather(location["latitude"], location["longitude"])
        print(f"Weather for {location['city']}, {location['country']}:")
        for temp, humidity, time in weather:
            print(f"{time}: {temp}°C, {humidity}% humidity")

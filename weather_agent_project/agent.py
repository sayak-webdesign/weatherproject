import requests
from google.adk.agents.llm_agent import Agent
from google.adk.agents import LlmAgent, SequentialAgent

def tool_get_coordinates(city: str) -> dict:
    """
    Gets the latitude and longitude for a given city name.
    Args:
        city (str): The name of the city (e.g., "New York").
    Returns:
        dict: A dictionary containing 'latitude' and 'longitude' or an 'error'.
    """
    try:
        url = "https://geocoding-api.open-Meteo.com/v1/search"
        params = {"name": city, "count": 1}
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        data = response.json()
        
        if "results" in data and len(data["results"]) > 0:
            location = data["results"][0]
            return {
                "status": "success",
                "city": city,
                "latitude": location["latitude"],
                "longitude": location["longitude"]
            }
        else:
            return {"status": "error", "error_message": f"Could not find coordinates for '{city}'."}
            
    except requests.exceptions.RequestException as e:
        return {"status": "error", "error_message": f"API request failed: {str(e)}"}

def tool_get_weather(latitude: float, longitude: float) -> dict:
    """
    Gets the current weather (temperature) for a given latitude and longitude.
    Args:
        latitude (float): The latitude.
        longitude (float): The longitude.
    Returns:
        dict: A dictionary containing the 'temperature' and 'unit' or an 'error'.
    """
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m",  # Get current temperature at 2 meters
            "temperature_unit": "celsius"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if "current" in data and "temperature_2m" in data["current"]:
            temp = data["current"]["temperature_2m"]
            unit = data["current_units"]["temperature_2m"]
            return {
                "status": "success",
                "temperature": temp,
                "unit": "°C" if unit == "celsius" else unit
            }
        else:
            return {"status": "error", "error_message": "Could not parse weather data."}
            
    except requests.exceptions.RequestException as e:
        return {"status": "error", "error_message": f"API request failed: {str(e)}"}

root_agent = LlmAgent(
    name="weather_bot_v1",
    model="gemini-2.5-flash", # Use a Gemini model
    description="A bot that can get the weather for a city.",
    
    # Give the agent access to both tools
    tools=[tool_get_coordinates, tool_get_weather],
    
    # The instruction must be very long and precise
    instruction=(
        "You are a helpful weather bot."
        "The user will give you a city name."
        "You MUST follow this two-step process:"
        "1. Use the 'tool_get_coordinates' tool to get the latitude and longitude for the city."
        "2. Once you have the coordinates, and ONLY once you have them, use the 'tool_get_weather' tool "
        "   with the 'latitude' and 'longitude' from the first tool's output."
        "3. Report the final temperature to the user."
        "Do not try to call 'tool_get_weather' with a city name. It will fail."
    )
)
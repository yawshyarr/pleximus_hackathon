import urllib.request
import urllib.parse
import json


def get_weather(city: str) -> str:
    try:
        geo_url = (
            f"https://geocoding-api.open-meteo.com/v1/search"
            f"?name={urllib.parse.quote(city)}&count=1"
        )
        with urllib.request.urlopen(geo_url, timeout=10) as resp:
            geo_data = json.loads(resp.read())

        results = geo_data.get("results")
        if not results or not isinstance(results, list) or len(results) == 0:
            return f"Error: city '{city}' not found"

        loc = results[0]
        lat = loc.get("latitude")
        lon = loc.get("longitude")
        if lat is None or lon is None:
            return f"Error: geocoding response for '{city}' missing coordinates"
        city_name = loc.get("name", city)

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
        )
        with urllib.request.urlopen(weather_url, timeout=10) as resp:
            weather_data = json.loads(resp.read())

        current = weather_data.get("current")
        if not current or not isinstance(current, dict):
            return f"Error: weather API returned unexpected data for '{city}'"

        temp = current.get("temperature_2m")
        humidity = current.get("relative_humidity_2m")
        wind = current.get("wind_speed_10m")
        code = current.get("weather_code")

        parts = []
        if temp is not None:
            parts.append(f"{temp}°C")
        if humidity is not None:
            parts.append(f"humidity {humidity}%")
        if wind is not None:
            parts.append(f"wind {wind} km/h")
        if code is not None:
            parts.append(f"code {code}")

        if not parts:
            return f"Error: weather data for '{city}' is empty"

        return f"Weather in {city_name}: {', '.join(parts)}"

    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        return f"Error: network request failed — {e}"
    except (json.JSONDecodeError, ValueError) as e:
        return f"Error: malformed API response — {e}"
    except Exception as e:
        return f"Error fetching weather: {e}"

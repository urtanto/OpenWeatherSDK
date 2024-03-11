import json
from datetime import datetime
from dataclasses import dataclass


def get_time_difference(time1: datetime, time2: datetime) -> float:
    """
    Calculates the absolute difference in seconds between two datetime objects.

    :param time1: The first datetime object.
    :param time2: The second datetime object.
    :return: The absolute difference in seconds between time1 and time2.
    """
    return abs((time2 - time1).total_seconds())


@dataclass
class WeatherData:
    """
    Contains weather data.

    :argument lat: float - Latitude of the location.
    :argument lon: float - Longitude of the location.
    :argument weather_main: str - Main weather condition.
    :argument weather_description: str - Detailed description of the weather.
    :argument temperature: float - Current temperature in Celsius.
    :argument temperature_feels_like: float - Feels-like temperature in Celsius.
    :argument visibility: int - Visibility distance in meters.
    :argument wind_speed: float - Wind speed in meters per second.
    :argument datetime: int - Date and time of the weather data as a Unix timestamp.
    :argument sunrise: int - Sunrise time as a Unix timestamp.
    :argument sunset: int - Sunset time as a Unix timestamp.
    :argument timezone: int - Timezone offset from UTC in seconds.
    :argument name: str - Name of the location (e.g., city name).
    """
    lat: float
    lon: float
    weather_main: str
    weather_description: str
    temperature: float
    temperature_feels_like: float
    visibility: int
    wind_speed: float
    datetime: int
    sunrise: int
    sunset: int
    timezone: int
    name: str

    def to_json(self) -> json:
        """
        Converts the WeatherData instance into a JSON string.

        :return: A JSON string representing the weather data.
        """
        data_dict = {
            "weather": {
                "main": self.weather_main,
                "description": self.weather_description
            },
            "temperature": {
                "temp": self.temperature,
                "feels_like": self.temperature_feels_like
            },
            "visibility": self.visibility,
            "wind": {
                "speed": self.wind_speed
            },
            "datetime": self.datetime,
            "sys": {
                "sunrise": self.sunrise,
                "sunset": self.sunset
            },
            "timezone": self.timezone,
            "name": self.name
        }

        return json.dumps(data_dict)

    def get_datetime(self) -> datetime:
        """
        Converts the Unix timestamp (self.datetime) to a datetime object.

        :return: A datetime object representing the date and time of the weather data.
        """
        return datetime.utcfromtimestamp(self.datetime)

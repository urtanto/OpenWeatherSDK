import json
from datetime import datetime
from dataclasses import dataclass


@dataclass
class WeatherData:
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
        return datetime.utcfromtimestamp(self.datetime)

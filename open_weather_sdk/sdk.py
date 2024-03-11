import json
import time
from datetime import datetime, timezone
import threading

import requests

from open_weather_sdk import WeatherData
from open_weather_sdk.exeptions import *


def get_time_difference(time1: datetime, time2: datetime) -> float:
    """
    Calculates the absolute difference in seconds between two datetime objects.
    :param time1: The first datetime object.
    :param time2: The second datetime object.
    :return: The absolute difference in seconds between time1 and time2.
    """
    return abs((time2 - time1).total_seconds())


class OpenWeatherSDK:
    """
    A class to interact with the OpenWeatherMap API.
    It ensures a single instance per API key and implements on-demand and pooling mode to update weather data.
    """
    __instances = {}

    def __new__(cls, apikey: str, *args, **kwargs):
        """
        Ensures only one instance of this class is created for each unique API key.
        Initializes the instance with API key and starts a pooling thread if necessary.
        :param apikey: The API key for authenticating requests to OpenWeatherMap.
        """
        if apikey not in cls.__instances:
            cls.__instances[apikey] = super(OpenWeatherSDK, cls).__new__(cls)
            cls.__instances[apikey].__api_key = apikey
            cls.__instances[apikey].__local_cache = dict()
            cls.__instances[apikey].__local_history = list()
            cls.__instances[apikey].__update_time = 10 * 60
            cls.__instances[apikey].__params = {
                'appid': cls.__instances[apikey].__api_key,
                "exclude": "minutely,hourly,daily,alerts",
                "units": "metric",
                "lang": "en",
            }
            cls.__instances[apikey].__poling = kwargs.get("polling", False)
            if cls.__instances[apikey].__poling:
                cls.__instances[apikey].__pooling_thread = threading.Thread(
                    target=cls.__instances[apikey].__pooling_cycle
                )
                cls.__instances[apikey].__pooling_thread.start()
        return cls.__instances[apikey]

    def __init__(self, apikey, **kwargs):
        """
        Initializes placeholder attributes for the instance. Actual initialization happens in __new__.
        :param apikey: The API key for the OpenWeatherMap API.
        """
        self.__api_key = self.__instances.get(apikey).__api_key
        self.__local_cache = self.__instances.get(apikey).__local_cache
        self.__local_history = self.__instances.get(apikey).__local_history
        self.__update_time = self.__instances.get(apikey).__update_time
        self.__params = self.__instances.get(apikey).__params
        self.__poling = self.__instances.get(apikey).__poling
        if self.__poling:
            self.__pooling_thread = self.__instances.get(apikey).__pooling_thread

    def get_update_time(self) -> int:
        """
        Returns the current update time interval for weather data pooling.
        :return: The update time interval in seconds.
        """
        return self.__update_time

    def set_update_time(self, update_time) -> None:
        """
        Sets a new update time interval for weather data pooling.
        :param update_time: The new update time interval in seconds.
        """
        self.__update_time = update_time

    def get_city_coordinates(self, city_name) -> (float, float):
        """
        Retrieves the latitude and longitude for a given city name.
        :param city_name: The name of the city.
        :return: A tuple containing the latitude and longitude of the city.
        """
        if city_name in self.__local_cache:
            return self.__local_cache[city_name].lat, self.__local_cache[city_name].lon
        url = f"http://api.openweathermap.org/geo/1.0/direct"
        params = {
            'q': city_name,
            'limit': 1,
            'appid': self.__api_key
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]['lat'], data[0]['lon']
            else:
                raise InvalidCity("Город не найден")
        elif response.status_code == 401:
            raise UnauthorizedError("Unauthorized access", response.json())
        elif response.status_code == 404:
            raise NotFoundError("Ресурс не найден", response.json())
        else:
            raise RequestError("Ошибка запроса к Geocoding API:", response.text)

    def get_weatherdata(self, city: str, lat: float = None, lon: float = None) -> json:
        """
        Retrieves or updates the weather data for a specified city.
        :param city: The name of the city.
        :param lat: The latitude of the city (optional if city name is provided).
        :param lon: The longitude of the city (optional if city name is provided).
        :return: A JSON object containing the weather data.
        """
        now = datetime.now(timezone.utc)
        if not (city in self.__local_cache and
                get_time_difference(
                    datetime.utcfromtimestamp(self.__local_cache[city].datetime).replace(tzinfo=timezone.utc), now
                ) < self.__update_time):
            with threading.Lock():
                params = self.__params.copy()
                if not lat and not lon:
                    lat, lon = self.get_city_coordinates(city)
                params["lat"] = lat
                params["lon"] = lon
                params["city_name"] = city
                if city not in self.__local_history:
                    self.__local_history.append(city)
                if len(self.__local_history) > 10:
                    del self.__local_cache[self.__local_history.pop(0)]
                self.__local_cache[city] = self.req_for_weatherdata(params)
        return self.__local_cache[city].to_json()

    @staticmethod
    def req_for_weatherdata(params: dict) -> WeatherData:
        """
        Makes a request to the OpenWeatherMap API to retrieve weather data for specific coordinates.
        :param params: A dictionary containing request parameters including latitude, longitude, and API key.
        :return: An instance of WeatherData containing the retrieved weather information.
        """
        url = "https://api.openweathermap.org/data/2.5/weather"
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            weather_data = WeatherData(
                lat=params["lat"],
                lon=params["lon"],
                weather_main=data["weather"][0]["main"],
                weather_description=data["weather"][0]["description"],
                temperature=data["main"]["temp"],
                temperature_feels_like=data["main"]["feels_like"],
                visibility=data["visibility"],
                wind_speed=data["wind"]["speed"],
                datetime=data["dt"],
                sunrise=data["sys"]["sunrise"],
                sunset=data["sys"]["sunset"],
                timezone=data["timezone"],
                name=params["city_name"]
            )
            return weather_data
        elif response.status_code == 401:
            raise UnauthorizedError("Unauthorized access", response.json())
        elif response.status_code == 404:
            raise NotFoundError("Ресурс не найден", response.json())
        else:
            raise RequestError("Ошибка получения данных от API:", response.status_code)

    def __pooling_cycle(self):
        """
       A continuous loop that updates cached weather data for all cities in the cache at set intervals.
       """
        while True:
            time.sleep(30)
            for city in self.__local_cache:
                city = self.__local_cache[city]
                now = datetime.now(timezone.utc)
                if get_time_difference(
                        city.get_datetime().replace(tzinfo=timezone.utc), now
                ) >= self.__update_time:
                    params = self.__params.copy()
                    city = self.__local_cache[city.name]
                    params["lat"] = city.lat
                    params["lon"] = city.lon
                    params["city_name"] = city.name
                    self.__local_cache[city.name] = self.req_for_weatherdata(params)

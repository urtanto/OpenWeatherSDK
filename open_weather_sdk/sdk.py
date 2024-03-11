import json
import time
from datetime import datetime, timezone
import threading

import requests

from open_weather_sdk import WeatherData
from open_weather_sdk.exeptions import *


def get_time_difference(time1: datetime, time2: datetime) -> float:
    return abs((time2 - time1).total_seconds())


class OpenWeatherSDK:
    __instances = {}

    def __new__(cls, apikey: str, *args, **kwargs):
        if apikey not in cls.__instances:
            cls.__instances[apikey] = super(OpenWeatherSDK, cls).__new__(cls)
            cls.__instances[apikey].__api_key = apikey
            cls.__instances[apikey].__local_cache = dict()
            cls.__instances[apikey].__update_time = 10 * 60
            cls.__instances[apikey].__params = {
                'appid': cls.__instances[apikey].__api_key,
                "exclude": "minutely,hourly,daily,alerts",
                "units": "metric",
                "lang": "en",
            }
            if "pooling" in kwargs and kwargs["pooling"]:
                cls.__instances[apikey].__pooling_thread = threading.Thread(
                    target=cls.__instances[apikey].__pooling_cycle
                )
                cls.__instances[apikey].__pooling_thread.start()
        return cls.__instances[apikey]

    def __init__(self, apikey, **kwargs):
        self.__api_key: str
        self.__local_cache: dict
        self.__update_time: int
        self.__params: dict
        self.__pooling_thread: threading.Thread

    def get_update_time(self) -> int:
        return self.__update_time

    def set_update_time(self, update_time) -> None:
        self.__update_time = update_time

    def get_city_coordinates(self, city_name) -> (float, float):
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
                self.__local_cache[city] = self.req_for_weatherdata(params)
        return self.__local_cache[city].to_json()

    @staticmethod
    def req_for_weatherdata(params: dict) -> WeatherData:
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

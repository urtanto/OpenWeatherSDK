import json
import time
import unittest
from datetime import datetime, timezone
from open_weather_sdk.sdk import OpenWeatherSDK, get_time_difference


def timer(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        res = func(*args, **kwargs)
        stop = datetime.now()
        return res, (stop - start).total_seconds()

    return wrapper


class TestOpenWeatherSDK(unittest.TestCase):

    def setUp(self):
        self.api_key = '4ddb12d67c931bb4d4bb26e7d8991f57'

    def test_same_object(self):
        sdk1 = OpenWeatherSDK(self.api_key)
        sdk2 = OpenWeatherSDK(self.api_key)
        self.assertIs(sdk1, sdk2)

    def test_get_time_difference(self):
        time1 = datetime(2021, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        time2 = datetime(2021, 1, 1, 12, 30, 0, tzinfo=timezone.utc)
        diff = get_time_difference(time1, time2)
        self.assertEqual(diff, 1800)

    def test_get_city_coordinates(self):
        sdk = OpenWeatherSDK(self.api_key)
        city_coordinates = sdk.get_city_coordinates("Saint Petersburg")
        self.assertEqual(city_coordinates, (59.938732, 30.316229))

    def test_get_weatherdata(self):
        sdk = OpenWeatherSDK(self.api_key)
        city_weatherdata = sdk.get_weatherdata("Saint Petersburg")
        city_weatherdata = json.loads(city_weatherdata)
        self.assertIn("weather", city_weatherdata)
        self.assertIn("main", city_weatherdata["weather"])
        self.assertIn("description", city_weatherdata["weather"])
        self.assertIn("temperature", city_weatherdata)
        self.assertIn("temp", city_weatherdata["temperature"])
        self.assertIn("feels_like", city_weatherdata["temperature"])
        self.assertIn("visibility", city_weatherdata)
        self.assertIn("wind", city_weatherdata)
        self.assertIn("speed", city_weatherdata["wind"])
        self.assertIn("datetime", city_weatherdata)
        self.assertIn("sys", city_weatherdata)
        self.assertIn("sunrise", city_weatherdata["sys"])
        self.assertIn("sunset", city_weatherdata["sys"])
        self.assertIn("timezone", city_weatherdata)
        self.assertIn("name", city_weatherdata)

    def test_cache(self):
        sdk = OpenWeatherSDK(self.api_key)
        for city in ["London", "New York", "Paris", "Tokyo", "Berlin", "Moscow", "Sydney", "Rome", "Madrid", "Toronto"]:
            city_weatherdata1, time1 = timer(sdk.get_weatherdata)(city)
            city_weatherdata2, time2 = timer(sdk.get_weatherdata)(city)
            self.assertLess(time2, time1)
        _, time1 = timer(sdk.get_weatherdata)("London")
        self.assertLess(time1, 1)
        _, _ = timer(sdk.get_weatherdata)("Saint Petersburg")
        _, time2 = timer(sdk.get_weatherdata)("London")
        self.assertLess(time1, time2)

    def test_pooling(self):
        sdk = OpenWeatherSDK(self.api_key, pooling=True)
        _, time1 = timer(sdk.get_weatherdata)("London")
        _, time2 = timer(sdk.get_weatherdata)("London")
        self.assertLess(time2, time1)
        time.sleep(10.5 * 60)
        _, time1 = timer(sdk.get_weatherdata)("London")
        self.assertGreater(time1, 1)
        _, time2 = timer(sdk.get_weatherdata)("London")
        self.assertLess(time2, time1)


if __name__ == '__main__':
    unittest.main()

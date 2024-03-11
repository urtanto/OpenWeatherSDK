import json
import time
import unittest
from datetime import datetime, timezone
from open_weather_sdk.sdk import OpenWeatherSDK, get_time_difference


def timer(func):
    """
    A decorator that measures the execution time of a function.

    :param func: The function to be decorated.
    :return: A wrapper function that returns the result of the decorated function and its execution time in seconds.
    """

    def wrapper(*args, **kwargs):
        start = datetime.now()
        res = func(*args, **kwargs)
        stop = datetime.now()
        return res, (stop - start).total_seconds()

    return wrapper


class TestOpenWeatherSDK(unittest.TestCase):
    """
    A set of unit tests for the OpenWeatherSDK class.
    """

    def setUp(self):
        self.api_key = '4ddb12d67c931bb4d4bb26e7d8991f57'

    def test_same_object(self):
        """
        Test that two instances of OpenWeatherSDK with the same API key are the same (Singleton pattern).
        """
        sdk1 = OpenWeatherSDK(self.api_key)
        sdk2 = OpenWeatherSDK(self.api_key)
        self.assertIs(sdk1, sdk2)

    def test_get_time_difference(self):
        """
        Test the get_time_difference function with two specific datetime objects.
        """
        time1 = datetime(2021, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        time2 = datetime(2021, 1, 1, 12, 30, 0, tzinfo=timezone.utc)
        diff = get_time_difference(time1, time2)
        self.assertEqual(diff, 1800)

    def test_get_city_coordinates(self):
        """
        Test getting the coordinates of a specific city using the SDK.
        """
        sdk = OpenWeatherSDK(self.api_key)
        city_coordinates = sdk.get_city_coordinates("Saint Petersburg")
        self.assertEqual(city_coordinates, (59.938732, 30.316229))

    def test_get_weatherdata(self):
        """
        Test retrieving weather data for a specific city and ensure that key data points are present in the response.
        """
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
        """
        Test that caching mechanism works by ensuring subsequent requests for the same city are faster than the first.
        """
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
        """
        Test that the pooling mechanism updates the cache at set intervals, making requests faster.
        """
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

import json
import time
import unittest
from unittest import mock
from unittest.mock import patch
from datetime import datetime, timezone
from open_weather_sdk.sdk import OpenWeatherSDK, get_time_difference


class TestOpenWeatherSDK(unittest.TestCase):
    """
    A set of unit tests for the OpenWeatherSDK class.
    """
    city_mocks = {'London': {'coord': {'lon': -0.1276, 'lat': 51.5073}, 'weather': [
        {'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations',
                             'main': {'temp': 12.13, 'feels_like': 11.67, 'temp_min': 10.97, 'temp_max': 12.85,
                                      'pressure': 1006, 'humidity': 87}, 'visibility': 10000,
                             'wind': {'speed': 4.63, 'deg': 250}, 'clouds': {'all': 75},
                             'dt': datetime.now(timezone.utc).timestamp(),
                             'sys': {'type': 2, 'id': 2075535, 'country': 'GB', 'sunrise': 1710483236,
                                     'sunset': 1710525891}, 'timezone': 0, 'id': 2643743, 'name': 'London',
                             'cod': 200}, 'New York': {'coord': {'lon': -74.006, 'lat': 40.7127}, 'weather': [
        {'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'base': 'stations',
                                                       'main': {'temp': 20.74, 'feels_like': 20.2,
                                                                'temp_min': 19.09, 'temp_max': 22, 'pressure': 1005,
                                                                'humidity': 51}, 'visibility': 10000,
                                                       'wind': {'speed': 8.23, 'deg': 280, 'gust': 16.46},
                                                       'clouds': {'all': 40},
                                                       'dt': datetime.now(timezone.utc).timestamp(),
                                                       'sys': {'type': 1, 'id': 4610, 'country': 'US',
                                                               'sunrise': 1710500817, 'sunset': 1710543765},
                                                       'timezone': -14400, 'id': 5128581, 'name': 'New York',
                                                       'cod': 200},
                  'Paris': {'coord': {'lon': 2.32, 'lat': 48.8589}, 'weather': [
                      {'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}],
                            'base': 'stations',
                            'main': {'temp': 13.66, 'feels_like': 13.22, 'temp_min': 11.02, 'temp_max': 14.49,
                                     'pressure': 1012, 'humidity': 82}, 'visibility': 10000,
                            'wind': {'speed': 6.17, 'deg': 240}, 'clouds': {'all': 75},
                            'dt': datetime.now(timezone.utc).timestamp(),
                            'sys': {'type': 2, 'id': 2041230, 'country': 'FR', 'sunrise': 1710482614,
                                    'sunset': 1710525339}, 'timezone': 3600, 'id': 6545270, 'name': 'Palais-Royal',
                            'cod': 200}, 'Tokyo': {'coord': {'lon': 139.7595, 'lat': 35.6828}, 'weather': [
            {'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations',
                                                   'main': {'temp': 12.02, 'feels_like': 10.58, 'temp_min': 7.3,
                                                            'temp_max': 13.87, 'pressure': 1013, 'humidity': 50},
                                                   'visibility': 10000, 'wind': {'speed': 8.75, 'deg': 350},
                                                   'clouds': {'all': 0},
                                                   'dt': datetime.now(timezone.utc).timestamp(),
                                                   'sys': {'type': 2, 'id': 268395, 'country': 'JP',
                                                           'sunrise': 1710535831, 'sunset': 1710578928},
                                                   'timezone': 32400, 'id': 1861060, 'name': 'Japan', 'cod': 200},
                  'Berlin': {'coord': {'lon': 13.3889, 'lat': 52.517},
                             'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}],
                             'base': 'stations',
                             'main': {'temp': 13.29, 'feels_like': 12.63, 'temp_min': 10.05, 'temp_max': 14.95,
                                      'pressure': 1007, 'humidity': 75}, 'visibility': 10000,
                             'wind': {'speed': 4.47, 'deg': 210, 'gust': 5.81}, 'clouds': {'all': 0},
                             'dt': datetime.now(timezone.utc).timestamp(),
                             'sys': {'type': 2, 'id': 2011538, 'country': 'DE', 'sunrise': 1710480012,
                                     'sunset': 1710522628}, 'timezone': 3600, 'id': 7576815, 'name': 'Alt-Kölln',
                             'cod': 200}, 'Moscow': {'coord': {'lon': 37.6175, 'lat': 55.7504}, 'weather': [
            {'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'base': 'stations',
                                                     'main': {'temp': 2.91, 'feels_like': -0.8, 'temp_min': 1.8,
                                                              'temp_max': 3.72, 'pressure': 1023, 'humidity': 93,
                                                              'sea_level': 1023, 'grnd_level': 1003},
                                                     'visibility': 10000,
                                                     'wind': {'speed': 4.15, 'deg': 219, 'gust': 7.75},
                                                     'clouds': {'all': 100},
                                                     'dt': datetime.now(timezone.utc).timestamp(),
                                                     'sys': {'type': 2, 'id': 2000314, 'country': 'RU',
                                                             'sunrise': 1710474259, 'sunset': 1710516753},
                                                     'timezone': 10800, 'id': 524901, 'name': 'Moscow', 'cod': 200},
                  'Sydney': {'coord': {'lon': 151.2083, 'lat': -33.8698}, 'weather': [
                      {'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}],
                             'base': 'stations',
                             'main': {'temp': 17.22, 'feels_like': 17.16, 'temp_min': 14.68, 'temp_max': 19.01,
                                      'pressure': 1021, 'humidity': 83}, 'visibility': 10000,
                             'wind': {'speed': 3.6, 'deg': 130}, 'clouds': {'all': 40},
                             'dt': datetime.now(timezone.utc).timestamp(),
                             'sys': {'type': 2, 'id': 2018875, 'country': 'AU', 'sunrise': 1710532513,
                                     'sunset': 1710576752}, 'timezone': 39600, 'id': 6619279, 'name': 'Sydney',
                             'cod': 200}, 'Rome': {'coord': {'lon': 12.4829, 'lat': 41.8933}, 'weather': [
            {'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations',
                                                   'main': {'temp': 13.79, 'feels_like': 12.9, 'temp_min': 12.07,
                                                            'temp_max': 14.86, 'pressure': 1020, 'humidity': 64},
                                                   'visibility': 10000, 'wind': {'speed': 2.06, 'deg': 180},
                                                   'clouds': {'all': 40},
                                                   'dt': datetime.now(timezone.utc).timestamp(),
                                                   'sys': {'type': 2, 'id': 2000926, 'country': 'IT',
                                                           'sunrise': 1710480096, 'sunset': 1710522979},
                                                   'timezone': 3600, 'id': 3169070, 'name': 'Rome', 'cod': 200},
                  'Madrid': {'coord': {'lon': -3.7036, 'lat': 40.4167},
                             'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}],
                             'base': 'stations',
                             'main': {'temp': 16.05, 'feels_like': 15.49, 'temp_min': 14.5, 'temp_max': 16.88,
                                      'pressure': 1022, 'humidity': 68}, 'visibility': 10000,
                             'wind': {'speed': 3.09, 'deg': 250}, 'clouds': {'all': 20},
                             'dt': datetime.now(timezone.utc).timestamp(),
                             'sys': {'type': 2, 'id': 2007545, 'country': 'ES', 'sunrise': 1710483960,
                                     'sunset': 1710526883}, 'timezone': 3600, 'id': 3117735, 'name': 'Madrid',
                             'cod': 200}, 'Toronto': {'coord': {'lon': -79.3839, 'lat': 43.6535}, 'weather': [
            {'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'base': 'stations',
                                                      'main': {'temp': 9.75, 'feels_like': 8.16, 'temp_min': 6.91,
                                                               'temp_max': 11.55, 'pressure': 1012, 'humidity': 68},
                                                      'visibility': 10000, 'wind': {'speed': 3.09, 'deg': 190},
                                                      'clouds': {'all': 100},
                                                      'dt': datetime.now(timezone.utc).timestamp(),
                                                      'sys': {'type': 1, 'id': 718, 'country': 'CA',
                                                              'sunrise': 1710502135, 'sunset': 1710545027},
                                                      'timezone': -14400, 'id': 6167863, 'name': 'Downtown Toronto',
                                                      'cod': 200},
                  "Saint Petersburg": {'coord': {'lon': 30.3162, 'lat': 59.9387}, 'weather': [
                      {'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'base': 'stations',
                                       'main': {'temp': 6.58, 'feels_like': 3.31, 'temp_min': 5.23,
                                                'temp_max': 7.33, 'pressure': 1007, 'humidity': 91},
                                       'visibility': 10000, 'wind': {'speed': 5, 'deg': 220},
                                       'rain': {'1h': 0.49}, 'clouds': {'all': 100},
                                       'dt': datetime.now(timezone.utc).timestamp(),
                                       'sys': {'type': 2, 'id': 197864, 'country': 'RU',
                                               'sunrise': 1710476089, 'sunset': 1710518428},
                                       'timezone': 10800, 'id': 519690, 'name': 'Novaya Gollandiya',
                                       'cod': 200},
                  }
    city_coords = {'London': (51.5073219, -0.1276474), 'New York': (40.7127281, -74.0060152),
                   'Paris': (48.8588897, 2.3200410217200766), 'Tokyo': (35.6828387, 139.7594549),
                   'Berlin': (52.5170365, 13.3888599), 'Moscow': (55.7504461, 37.6174943),
                   'Sydney': (-33.8698439, 151.2082848), 'Rome': (41.8933203, 12.4829321),
                   'Madrid': (40.4167047, -3.7035825), 'Toronto': (43.6534817, -79.3839347),
                   "Saint Petersburg": (59.938732, 30.316229)}

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

    @patch('open_weather_sdk.sdk.requests.get')
    def test_get_city_coordinates(self, mock_get):
        """
        Test getting the coordinates of a specific city using the SDK.
        """
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'name': 'Saint Petersburg',
                                            'local_names': {'lv': 'Sanktpēterburga',
                                                            'hr': 'Sankt Peterburg',
                                                            'kn': 'ಸಂಕ್ತ್ ಪೇಟೆರ್ಬುಗ್',
                                                            'ku': 'Sankt Petersburg',
                                                            'nl': 'Sint-Petersburg',
                                                            'da': 'Sankt Petersborg',
                                                            'gl': 'San Petersburgo',
                                                            'ro': 'Sankt Petersburg',
                                                            'it': 'San Pietroburgo',
                                                            'sv': 'Sankt Petersburg',
                                                            'sl': 'Sankt Peterburg',
                                                            'fi': 'Pietari',
                                                            'hu': 'Szentpétervár',
                                                            'be': 'Санкт-Пецярбург',
                                                            'zh': '聖彼得堡/圣彼得堡',
                                                            'hi': 'सेंट पीटर्सबर्ग',
                                                            'sr': 'Санкт Петербург',
                                                            'lt': 'Sankt Peterburgas',
                                                            'ar': 'سانت بطرسبرغ',
                                                            'fa': 'سن پترزبورگ',
                                                            'ml': 'സെന്റ് പീറ്റേഴ്സ്ബർഗ്',
                                                            'mr': 'सेंट पीटर्सबर्ग',
                                                            'en': 'Saint Petersburg',
                                                            'vi': 'Xanh Pê-téc-bua',
                                                            'te': 'సెయింట్ పీటర్స్\u200cబర్గ్',
                                                            'el': 'Αγία Πετρούπολη',
                                                            'os': 'Бетъырбух',
                                                            'fr': 'Saint-Pétersbourg',
                                                            'uk': 'Санкт-Петербург',
                                                            'nb': 'Sankt Petersburg',
                                                            'eo': 'Sankt-Peterburgo',
                                                            'ca': 'Sant Petersburg',
                                                            'lb': 'Sankt Péitersbuerg',
                                                            'ab': 'Санқт-Петербург',
                                                            'ko': '상트페테르부르크',
                                                            'sk': 'Petrohrad',
                                                            'hy': 'Սանկտ Պետերբուրգ',
                                                            'ascii': 'Sankt-Peterburg',
                                                            'ja': 'サンクト ペテルブルク',
                                                            'feature_name': 'Sankt-Peterburg',
                                                            'et': 'Peterburi',
                                                            'pl': 'Petersburg',
                                                            'oc': 'Sant Petersborg',
                                                            'de': 'Sankt Petersburg',
                                                            'cs': 'Petrohrad',
                                                            'ru': 'Санкт-Петербург',
                                                            'ka': 'სანქტ-პეტერბურგი',
                                                            'es': 'San Petersburgo',
                                                            'pt': 'São Petersburgo',
                                                            'mk': 'Санкт Петербург',
                                                            'fy': 'Sint-Petersburch'},
                                            'lat': 59.938732, 'lon': 30.316229,
                                            'country': 'RU', 'state': 'Saint Petersburg'}]
        mock_get.return_value = mock_response

        sdk = OpenWeatherSDK(self.api_key)
        city_coordinates = sdk.get_city_coordinates("Saint Petersburg")
        self.assertEqual((59.938732, 30.316229), city_coordinates)

    @patch('open_weather_sdk.sdk.requests.get')
    @patch('open_weather_sdk.sdk.OpenWeatherSDK.get_city_coordinates')
    def test_get_weatherdata(self, mock_get_city_coordinates, mock_get):
        """
        Test retrieving weather data for a specific city and ensure that key data points are present in the response.
        """
        mock_get_city_coordinates.return_value = (59.938732, 30.316229)
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'coord': {'lon': 30.3162, 'lat': 59.9387}, 'weather': [
            {'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'base': 'stations',
                                                   'main': {'temp': 6.58, 'feels_like': 3.31, 'temp_min': 5.23,
                                                            'temp_max': 7.33, 'pressure': 1007, 'humidity': 91},
                                                   'visibility': 10000, 'wind': {'speed': 5, 'deg': 220},
                                                   'rain': {'1h': 0.49}, 'clouds': {'all': 100},
                                                   'dt': datetime.now(timezone.utc).timestamp(),
                                                   'sys': {'type': 2, 'id': 197864, 'country': 'RU',
                                                           'sunrise': 1710476089, 'sunset': 1710518428},
                                                   'timezone': 10800, 'id': 519690, 'name': 'Novaya Gollandiya',
                                                   'cod': 200}

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

    @patch('open_weather_sdk.sdk.requests.get')
    @patch('open_weather_sdk.sdk.OpenWeatherSDK.get_city_coordinates')
    def test_cache(self, mock_get_city_coordinates, mock_get: mock.Mock):
        """
        Test that caching mechanism works by ensuring subsequent requests for the same city are faster than the first.
        """
        city_coords = self.city_coords
        city_mocks = self.city_mocks

        sdk = OpenWeatherSDK(self.api_key)
        for city in ["London", "New York", "Paris", "Tokyo", "Berlin", "Moscow", "Sydney", "Rome", "Madrid", "Toronto"]:
            mock_get.reset_mock(return_value=True, side_effect=True)
            mock_get_city_coordinates.return_value = city_coords[city]
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = city_mocks[city]

            sdk.get_weatherdata(city)
            sdk.get_weatherdata(city)
            mock_get.assert_called_once()

        mock_get.reset_mock(return_value=True, side_effect=True)

        mock_get_city_coordinates.return_value = city_coords["Saint Petersburg"]
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = city_mocks["Saint Petersburg"]

        sdk.get_weatherdata("Saint Petersburg")
        sdk.get_weatherdata("Saint Petersburg")
        mock_get.assert_called_once()

    @patch('open_weather_sdk.sdk.requests.get')
    @patch('open_weather_sdk.sdk.OpenWeatherSDK.get_city_coordinates')
    def test_pooling(self, mock_get_city_coordinates, mock_get: mock.Mock):
        """
        Test that the pooling mechanism updates the cache at set intervals, making requests faster.
        """
        city_coords = self.city_coords
        city_mocks = self.city_mocks

        mock_get_city_coordinates.return_value = city_coords["London"]
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = city_mocks["London"]

        sdk = OpenWeatherSDK(self.api_key, pooling=True)
        sdk.get_weatherdata("London")
        sdk.get_weatherdata("London")
        mock_get.assert_called_once()
        time.sleep(10.5 * 60)
        mock_get.reset_mock(return_value=True, side_effect=True)
        mock_get_city_coordinates.return_value = city_coords["London"]
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = city_mocks["London"]
        mock_get.return_value.json.return_value["dt"] = datetime.now(timezone.utc).timestamp()
        sdk.get_weatherdata("London")
        sdk.get_weatherdata("London")
        mock_get.assert_called_once()


if __name__ == '__main__':
    unittest.main()

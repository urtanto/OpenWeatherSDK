# OpenWeatherSDK

The OpenWeatherSDK provides a convenient way to interact with the OpenWeatherMap API, enabling developers to easily integrate weather data into their applications. This SDK supports retrieving current weather data, forecasts, and historical weather information for any location provided by the user.

## Features

- Easy-to-use methods for getting weather data using the OpenWeatherMap API.
- Support for current weather data.
- Singleton pattern to ensure a single instance per API key.
- On-demand and pooling mode to update weather data efficiently.

## Installation

To install the OpenWeatherSDK, you will need to clone this repository and install the required dependencies listed in `requirements.txt`.

```bash
git clone https://github.com/urtanto/OpenWeatherSDK.git
cd OpenWeatherSDK
pip install -r requirements.txt
```

## Quick Start

To get started with the OpenWeatherSDK, you need to first obtain an API key from [OpenWeatherMap](https://openweathermap.org/api).

Here is a simple example on how to use the SDK to retrieve current weather data for a specific location:

```python
from open_weather_sdk.sdk import OpenWeatherSDK

# Initialize the SDK with your API key
api_key = "your_api_key_here"
sdk = OpenWeatherSDK(api_key)

# Retrieve current weather data for a location
location = "London"
weather_data = sdk.get_weatherdata(location)

print(weather_data)
```

## Handling Exceptions

The SDK defines several custom exceptions to handle various error conditions. It is recommended to wrap your calls in try-except blocks to manage potential errors gracefully.

```python
from open_weather_sdk.sdk import OpenWeatherSDK
from open_weather_sdk.exeptions import *

api_key = "your_api_key_here"
sdk = OpenWeatherSDK(api_key)

try:
    weather_data = sdk.get_current_weather("London")
except NotFoundError as e:
    print(f"NotFound error: {e}")
except UnauthorizedError as e:
    print(f"Unauthorized error: {e}")
except RequestError as e:
    print(f"Request error: {e}")
except APIError as e:
    print(f"API Key error: {e}")
```

import json
import time
from datetime import datetime, timedelta

from open_weather_sdk.sdk import OpenWeatherSDK


def timer(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        func(*args, **kwargs)
        stop = datetime.now()
        print(f"Working time: {(stop - start).total_seconds()}")

    return wrapper


@timer
def req(api_key):
    owsdk = OpenWeatherSDK(api_key)
    ans = owsdk.get_weatherdata("Saint Petersburg")
    ans = json.loads(ans)
    print(ans)
    dt_utc = datetime.utcfromtimestamp(ans["datetime"])
    print(dt_utc + timedelta(seconds=ans["timezone"]))


def main(api_key):
    owsdk = OpenWeatherSDK(api_key, pooling=True)
    # owsdk = OpenWeatherSDK(api_key)
    req(api_key)
    req(api_key)
    time.sleep(10 * 60)
    print("Wait: \\/\\/\\/\\/")
    time.sleep(1 * 60)
    req(api_key)
    req(api_key)


if __name__ == '__main__':
    main('4ddb12d67c931bb4d4bb26e7d8991f57')

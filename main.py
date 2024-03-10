import json
import time
from datetime import datetime, timedelta

from open_weather_sdk.sdk import OpenWeatherSDK


def req(api_key):
    owsdk = OpenWeatherSDK(api_key)
    ans = owsdk.get_weatherdata("Saint Petersburg")
    ans = json.loads(ans)
    print(ans)
    dt_utc = datetime.utcfromtimestamp(ans["datetime"])
    print(dt_utc + timedelta(seconds=ans["timezone"]))


def main(api_key):
    req(api_key)
    req(api_key)
    time.sleep(11 * 60)
    req(api_key)
    req(api_key)

    # print(owsdk.get_weatherdata("London", lat=51.5073219, lon=-0.1276474))


if __name__ == '__main__':
    main('4ddb12d67c931bb4d4bb26e7d8991f57')

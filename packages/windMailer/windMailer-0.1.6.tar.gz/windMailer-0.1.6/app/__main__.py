#!/usr/bin/env python
import forecastio
import slackweb
import sys
from __configure__ import *


def run():

    w = ""  # initializing in global context

    # fetching weather
    forecast = forecastio.load_forecast(forecast_key, lat, lng)
    by_day = forecast.daily()

    for dailyData in by_day.data:
        wind = dailyData.windSpeed
        time = dailyData.time
        wind_message = "Wind is expected to be " + str(wind) + "mph on " + str(time.strftime("%A\n"))

        if wind > 8:
            w += wind_message

    slack = slackweb.Slack(url=web_hook)
    slack.notify(text=w, channel=slack_channel)


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    run()


if __name__ == "__main__":
    main()

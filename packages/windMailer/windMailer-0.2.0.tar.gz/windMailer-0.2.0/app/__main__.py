#!/usr/bin/env python
import os
import forecastio
import slackweb
import sys
import ConfigParser

# initializing Config Parser
properties = os.path.join(os.path.dirname(__file__), 'properties')
Config = ConfigParser.ConfigParser()
Config.read(properties)


def set_config_file(property_header, property_value, property_name):
    if not Config.get(property_header, property_value):
        i = raw_input("Please enter " + property_name + ": \n")
        Config.set(property_header, property_value, i)


# setting config file if not already configured
set_config_file("API_KEYS", "web_hook", "Slack Web Hook")
set_config_file("API_KEYS", "forecast_key", "ForecastIO Api Key [https://darksky.net/dev/account]")
set_config_file("SLACK", "slack_channel", "Slack Channel")
with open('properties', 'w') as configfile:
    Config.write(configfile)

# initializing variables
web_hook = Config.get("API_KEYS", "web_hook")
forecast_key = Config.get("API_KEYS", "forecast_key")
slack_channel = Config.get("SLACK", "slack_channel")
lat = Config.get("VARS", "lat")
lng = Config.get("VARS", "lng")


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

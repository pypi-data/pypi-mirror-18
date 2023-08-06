import ConfigParser


def set_config_file(property_header, property_value, property_name):
    changed = False
    if not Config.get(property_header, property_value):
        i = raw_input("Please enter " + property_name + ": ")
        Config.set(property_header, property_value, i)
        changed = True

    if changed:
        print "Now that your configuration is set,\n please be sure to run the following git command: " \
              "\n\n\ngit update-index --assume-unchanged properties' this the windMailer dir"

# initializing Config Parser
Config = ConfigParser.ConfigParser()
Config.read("properties")

# setting config file if not already configured
set_config_file("API_KEYS", "web_hook", "Slack Web Hook")
set_config_file("API_KEYS", "forecast_key", "ForecastIO (Darksky) Api Key")
set_config_file("SLACK", "slack_channel", "Slack Channel (include #)")
with open('properties', 'w') as configfile:
    Config.write(configfile)

# initializing variables
web_hook = Config.get("API_KEYS", "web_hook")
forecast_key = Config.get("API_KEYS", "forecast_key")
slack_channel = Config.get("Slack", "slack_channel")
lat = Config.get("VARS", "lat")
lng = Config.get("VARS", "lng")

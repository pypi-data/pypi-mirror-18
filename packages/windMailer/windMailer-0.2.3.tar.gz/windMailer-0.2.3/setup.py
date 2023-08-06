from setuptools import setup

setup(
    # Application name:
    name="windMailer",

    # Version number (initial):
    version="0.2.3",

    # Application author details:
    author="dukeman",
    author_email="gabeduke@gmail.com",

    # Packages
    packages=["app"],

    scripts=['bin/windMailer.sh'],

    # Include additional files into the package
    include_package_data=True,

    # Details
     url="http://pypi.python.org/pypi/windMailer_v023/",

    #
    # license="LICENSE.txt",
    description="Useful towel-related stuff. ",

    # entry_points={
    #     'console_scripts': [
    #         'windMailer = app.__main__:run'
    #     ]
    # },

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "slackweb", "python-forecastio", "ConfigParser"

    ],

)

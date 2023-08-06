from setuptools import setup

setup(
    # Application name:
    name="windMailer",

    # Version number (initial):
    version="0.1.8",

    # Application author details:
    author="dukeman",
    author_email="gabeduke@gmail.com",

    # Packages
    packages=["app"],

    # Include additional files into the package
    include_package_data=True,

    # Details
     url="http://pypi.python.org/pypi/windMailer_v018/",

    #
    # license="LICENSE.txt",
    description="Useful towel-related stuff. ",

    entry_points={
        'console_scripts': [
            'windMailer = windMailer.app.__main__.py:run'
        ]
    },

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "slackweb", "python-forecastio", "ConfigParser"

    ],

)

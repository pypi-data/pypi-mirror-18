ftweet
======

|pypi badge| |downloads badge|

.. |pypi badge| image:: https://img.shields.io/pypi/v/ftweet.svg?maxAge=3600
   :target: https://pypi.python.org/pypi/ftweet/
.. |downloads badge| image:: https://img.shields.io/pypi/dm/ftweet.svg?maxAge=3600
   :target: https://pypi.python.org/pypi/ftweet/

Introduction
------------
This is a simple python script that allows you to tweet status updates from
the command line.

The script will post each line of a file (such as standard input) as an
individual status update. If a line is more than 140 characters in length, the
update may fail. The script can automatically truncate a line to this limit with
the ``--truncate`` command line option.

This script performs no interpretation of the input nor any scrubbing of the
text for special characters.

Prerequisites
-------------
* Python 2.7 or 3.0+
* Python tweepy library

Installation
------------

The module can be installed using the setup script:::

    sudo python setup.py install

This will install the ftweet.py module and an ftweet executable script.

Configuration
-------------
The authentication tokens used to access Twitter are stored separately from
the python script in a JSON file. This contains tokens and secrets for both
the API and access tokens. These access tokens can be configured by creating
a Twitter App (https://apps.twitter.com).

The configuration file must have the following format:::

    {
        "api_key": <consumer key (API key) string>,
        "api_secret": <consumer secret (API secret) string>,
        "token": <access token string>,
        "token_secret": <access token secret string>
    }

Note that the keys must be quoted strings. See http://json.org for more
information about the JSON format.

By default, ftweet looks for the configuration file in the user's home
directory named ``~/.ftweet``. You can also pass in a configuration file
using command line argument ``--config``.

Example Use
-----------
The genesis of this project was the desire to post Snort alerts to Twitter.
What good are intrusion alerts if they don't show up on your smartphone? The
ftweet script is designed to be used in conjunction with other BSD/Linux
utilities, or stand-alone on the command line.

Tweeting a simple status update:::

    echo "Hello World!" | ftweet

Monitoring for sudo events from the sylog, truncating the line if necessary:::

    tail -f /var/log/auth.log | grep sudo | ftweet --truncate

Using in combination with swatch to monitor for snort alerts. The ``~/.swatchrc``
file may look like:::

    watchfor /snort\[\d{1,5}\]:/
    pipe /bin/sed -r -f ~/snort/my_scrub_rules.sed | ftweet --truncate


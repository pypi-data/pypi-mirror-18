"""
Copyright (c) 2016 Stefan R. Filipek
Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import re
import sys
import json
import tweepy
import os.path
import fileinput


def tweet(iterable, access, truncate=False):
    """Tweet status updates from the given iterable object.
    
    Args:
        iterable:   Interable object of strings to tweet
        access:     A twitter access dictionary

    The access dictionary must be strucured as:
        {
            "api_key": <consumer key (API key) string>,
            "api_secret": <consumer secret (API secret) string>,
            "token": <access token string>,
            "token_secret": <access token secret string>
        }
    """
    # Setup the authentication
    auth = tweepy.OAuthHandler(access["api_key"], access["api_secret"])
    auth.set_access_token(access["token"], access["token_secret"])

    # Setup the API
    api = tweepy.API(auth)

    # Tweet every status update
    for status in iterable:
        if truncate:
            status = status[:140]

        #print("Tweeting '{status}'".format(status=status))
        api.update_status(status)


def main():
    import argparse

    # Build up arguments
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--file',
        default='-',
        help='Path to the input file (defaults to stdin)')

    parser.add_argument(
        '--config',
        default=os.path.expanduser('~/.ftweet'),
        help='Path to the twitter config JSON file (defaults to ~/.ftweet)')

    parser.add_argument(
        '--truncate',
        default=False,
        action='store_true',
        help='Automatically truncate to 140 characters before posting')

    # Parse
    args = parser.parse_args()

    # Get the auth configuration
    with open(args.config, "r") as fobj:
        access = json.load(fobj)

    # Tweet!
    stati = (line.strip() for line in fileinput.input((args.file,)))
    tweet(stati, access, args.truncate)


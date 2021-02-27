#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import json
from pytz import UTC
from tweepy.streaming import Stream, StreamListener
from typing import List
import twint
import sys

from StockSight.TweetStreamListener import logger
class TwintStream(Stream):
    def __init__(self, listener: StreamListener):
        self.listener = listener

    # Start the stream
    # feeds is a list of usernames
    def filter(self, feeds: List[str] = ['@elonmusk']):

        twint_config = twint.Config()

        # Create the query
        custom_query = ''.join([f'from:{feed} OR ' for feed in feeds])
        twint_config.Custom_query = custom_query

        # Override default json serializing
        def Json(obj, config):

            # Cleanup the useless stuff
            tweet = obj.__dict__

            # Proper dates
            try:
                dt = UTC.localize(datetime.strptime(
                    tweet['datetime'], twint.tweet.Tweet_formats['datetime']))
                created_at = datetime.strftime(dt, '%a %b %d %H:%M:%S +0000 %Y')
            except Exception as e:
                logger.error(e)
                return

            # Object to send
            to_send = {
                'text': tweet.tweet,
                'created_at': created_at,
                'id': tweet.id,
                'user': {
                    'screen_name': tweet.username,
                    'location': tweet.place,
                    'lang': tweet.lang,
                    'friends_count': -1,
                    'followers_count': -1,
                    'statuses_count': -1,
                }
            }

            # Convert the data to json
            raw_data = json.dumps(to_send)

            # Send the "raw data" to the stream listener
            self.listener.on_data(raw_data)
        sys.modules["twint.storage.write"].Json = Json
        twint_config.Output = "tweets.json"  # Necessary
        twint_config.Store_json = True  # Necessary

        # No spam
        twint_config.Hide_output = True

        # Run the stream
        twint.run.Search(twint_config)

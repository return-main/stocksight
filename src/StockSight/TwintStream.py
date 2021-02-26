#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tweepy.streaming import Stream, StreamListener
from typing import List, String
import twint

class TwintStream(Stream):
    def __init__(self, listener: StreamListener):
        self.listener = listener

    # Start the stream
    # feeds is a list of usernames
    def filter(self, feeds: List[String] = ['@elonmusk']):
        custom_query = ''.join([ f'from:{feed} OR ' for feed in feeds ])

        twint_config = twint.Config(Custom_query=custom_query)
        twint.run.Search(twint_config)

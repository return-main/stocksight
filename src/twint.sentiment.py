#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tweet sentiment runner
See README.md or https://github.com/shirosaidev/stocksight
for more information.

Copyright (C) Chris Park 2018-2019
Copyright (C) Allen (Jian Feng) Xie 2019
stocksight is released under the Apache 2.0 license. See
LICENSE for the full license text.
"""

import sys

from StockSight.TweetStreamListener import TweetStreamListener, logger, config, es
from StockSight.EsMap.Sentiment import mapping

from StockSight.TwintStream import TwintStream

import time
from pytz import UTC
from os import environ

STOCKSIGHT_VERSION = '0.2'
__version__ = STOCKSIGHT_VERSION


if __name__ == '__main__':

    # Set timezone to UTC (To have the correct timestamps)
    environ['TZ'] = UTC.zone
    time.tzset()

    twitter_feeds = config['twitter']['feeds']

    try:
        for symbol in config['twitter']:
            logger.info(
                'Creating new Elasticsearch index or using existing ' + symbol)
            es.indices.create(index="stocksight_"+symbol+"_sentiment", body=mapping, ignore=[400, 404])

        # create instance of TweetStreamListener
        TweetStreamListener = TweetStreamListener()

        # create instance of the tweepy stream
        stream = TwintStream(TweetStreamListener)

        # search twitter for keywords
        logger.info('NLTK tokens required: ' + str(config['symbols']))
        logger.info('NLTK tokens ignored: ' +
                    str(config['sentiment_analyzer']['ignore_words']))
        logger.info('Twitter Feeds: ' + str(twitter_feeds))
        logger.info('Listening for Tweets (ctrl-c to exit)...')

        stream.filter(feeds=twitter_feeds)
    # except TweepError as te:
    #     logger.debug(
    #         "Tweepy Exception: Failed to get tweets caused by: %s" % te)
    except KeyboardInterrupt:
        print("Ctrl-c keyboard interrupt, exiting...")
        stream.disconnect()
        sys.exit(0)
    except Exception as e:
        logger.warning("%s" % e)

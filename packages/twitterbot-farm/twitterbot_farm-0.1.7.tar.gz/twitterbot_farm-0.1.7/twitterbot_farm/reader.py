#!/usr/bin/env python
from bot import Bot


class Reader(Bot):
    """ Reads fead and stores them into redis db. """

    def __init__(self, username, host='127.0.0.1'):
        Bot.__init__(self, username, host)
        self.last_tweet_id = int(self.connection.get('__last_tweet_id__', 1))

    def save(self, tweet_list):
        for tweet in tweet_list:
            self.connection[tweet.id] = tweet.text
        self.connection['__last_tweet_id__'] = self.last_tweet_id

    def fetch(self):
        tweet_list = self.twibot.api.home_timeline(since_id=self.last_tweet_id, count=200)
        self.last_tweet_id = max(tweet.id for tweet in tweet_list)
        self.save(tweet_list)

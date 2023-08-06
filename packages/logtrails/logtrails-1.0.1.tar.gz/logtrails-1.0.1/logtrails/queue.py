"""
Redis connection and pubsub queue handling
"""

import redis
from redis.exceptions import ConnectionError


class QueueError(Exception):
    pass


class RedisConnection(redis.StrictRedis):
    """Connection to configured redis server

    Default pubsub channel names can be specified in channels argument.

    self.pubsub() will subscribe to configured channels automatically.

    If you wish to use pattern subscriptions, do it yourself with the self.pubsub() object
    """

    def __init__(self, hostname, port, channels=[]):
        super(RedisConnection, self).__init__(host=hostname, port=port)
        self.channels = channels

    def pubsub(self, ignore_subscribe_messages=True):
        """Override default pubsub with autosubscribing version

        This version ignores subscribe/unsubscribe messages by default.

        Creates normal pubsub object and registers self.channels automatically to
        the returned object.
        """

        try:
            pubsub = super(RedisConnection, self).pubsub(ignore_subscribe_messages=ignore_subscribe_messages)
            for channel in self.channels:
                pubsub.subscribe(channel)
        except ConnectionError as e:
            raise QueueError('Error subscribing to redis pubsub channels: {0}'.format(e))

        return pubsub

from redis import StrictRedis
from typing import Union


def load(host='127.0.0.1', port=6379):
    """
    Open a connection to Redis.

    :param host: Redis' server IP
    :param port: Redis' server port
    :return: Redis connection object.
    """
 
    connection = StrictRedis(host=host, port=port)
    return connection


class RedisMixin:
    """
    Mixin for Redis classes.

    Brings objectification to classes that are kept on a Redis DB.
    """
    def __init__(self, item_id: str, redis_inst: StrictRedis):
        self.item_id = item_id
        self.redis = redis_inst
        self.key = None

        #  Set the redis key to True if the item doesn't exist and notifies us about whether it's new or not.
        self.was_just_created = self.init()

    @property
    def exists(self) -> bool:
        return bool(self.redis.get('{}/{}'.format(self.key, self.item_id)))

    def init(self) -> bool:
        if not self.exists:
            self.redis.set('{}/{}'.format(self.key, self.item_id), True)
            return True
        return False

    def reset(self):
        for key in self.scan():
            self.redis.delete(key)

    def fetch(self, key) -> Union[str, int]:
        value = self.redis.get('{}/{}/{}'.format(
            self.key,
            self.item_id,
            key
        ))
        if value:
            return value.decode('utf-8')

    def scan(self, key=None):
        if not key:
            return [k for k in self.redis.scan_iter(match='{}/{}*'.format(
                self.key,
                self.item_id,
            ))] or []
        return [k for k in self.redis.scan_iter(match='{}/{}/{}*'.format(
            self.key,
            self.item_id,
            '{}'.format(key)
        ))] or []

    def update(self, key, value):
        self.redis.set('{}/{}/{}'.format(
            self.key,
            self.item_id,
            key
        ), value)

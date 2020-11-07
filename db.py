import redis
import os

REDIS_URL = os.environ.get('REDIS_URL')

class DB:

    def __init__(self, primary_key_name, set_name):
        if REDIS_URL:
            self.r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
        else:
            self.r = redis.Redis(decode_responses=True)
        # set_name is the name of the redis set to which hashes will be added as members
        # primary_key_name is the dictionary key that will also be the redis key for the hash of values
        self.primary_key_name = primary_key_name
        self.set_name = set_name

    def fetchall(self):
        out = []
        for key in self.r.smembers(self.set_name):
            out.append(self.r.hgetall(key))
        return out

    def fetch(self, key):
        return self.r.hgetall(key)

    def add(self, d):
        assert isinstance(d, dict)
        if self.primary_key_name not in d:
            raise ValueError("{} not found in dict".format(self.primary_key_name))
        key = d[self.primary_key_name]
        for _k, _v in d.items():
            self.r.hset(key, _k, _v)
        self.r.sadd(self.set_name, key)

    def delete(self, key):
        self.r.delete(key)


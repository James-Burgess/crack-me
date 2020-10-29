import os
from multiprocessing import Pool

from pymongo import MongoClient
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "redis://localhost")

class RedisQueue(object):
    """Simple Queue with Redis Backend"""

    def __init__(self, name, namespace="queue", **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db = redis.Redis(REDIS_HOST)
        self.key = "%s:%s" % (namespace, name)

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.__db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item):
        """Put item into the queue."""
        self.__db.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.

        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)

        if item:
            item = item[1]
        return item

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)


def increment_attempt_count(user, db):
    stored_user = db.users.find_one({"user": user.decode()})
    db.users.update_one(
        {"_id": stored_user["_id"]}, {"$inc": {"count": 1}}, upsert=False
    )
    print(stored_user)

def listen(_):
    client = MongoClient(
        os.getenv("MONGO_DB_URL")
    )
    db = client.users
    q = RedisQueue("test")
    print('alive')
    while True:
        e = q.get()
        if e:
            increment_attempt_count(e, db)


if __name__ == "__main__":
    with Pool(processes=4) as pool:
        pool.map(listen, range(10))

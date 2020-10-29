import os
from collections import OrderedDict
from datetime import datetime

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


client = MongoClient(
    os.getenv("MONGO_DB_URL")
)
db = client.users

class UserMemo(OrderedDict):
    def __init__(self, *args, **kwds):
        self.size_limit = kwds.pop("size_limit", None)
        OrderedDict.__init__(self, *args, **kwds)
        self._check_size_limit()

    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self, key, value)
        self._check_size_limit()

    def _check_size_limit(self):
        if self.size_limit is not None:
            while len(self) > self.size_limit:
                self.popitem(last=False)


user_memo = UserMemo(size_limit=10)
def get_or_create_user(user, hash, browser):
    stored_user = user_memo.get(user) or db.users.find_one({"user": user})
    user_memo[user] = stored_user

    if hash and stored_user:
        if stored_user.get("hash") != hash:
            return None
        return user
    elif stored_user:
        return user
    elif not hash:
        return None
    elif db.users.find_one({"hash": hash}):
        return None
    elif browser:
        db.users.insert_one({"user": user, "hash": hash, "count": 0})
        return user
    else:
        return None

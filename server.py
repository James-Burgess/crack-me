import os
from datetime import datetime

from bottle import (
    auth_basic,
    request,
    route,
    error,
    static_file,
    run,
    abort,
    default_app,
    HTTPError,
    view
)
import redis

from worker import RedisQueue
from request_utils import interceptor
from user import db

incrementor = RedisQueue('test')

def check_credentials(user, pw):
    incrementor.put(user)
    password = os.getenv("ITS_AN_ENV_VAR_BRO")
    print(pw)
    return pw == password


@route("/locked")
@interceptor(check_credentials)
@view('win')
def win(user):
    user = db.users.find_one({"user": user})
    print(user)
    solve_time = datetime.now().strftime('%s')
    if not user.get("solved"):
        db.users.update_one(
            {"_id": user["_id"]}, {"$set": {"solved": True, "solve_time": solve_time}}, upsert=False
        )
        user = db.users.find_one({"user": user})
    sign_up = user.get("sign_up")
    duration = int(user.get(solve_time, 0)) - int(sign_up or 0) * 60 * 60
    pos = db.users.count_documents(({"count": { "$lte" : user.get('count')}, "solved": True})) + 1
    return {
        "sign_up": datetime.fromtimestamp(int(sign_up or 0)),
        "count": user.get('count'),
        "duration": duration,
        "postion": pos,
        "total_users":  db.command("collstats", "users").get('count'),
        "total_winners": db.users.count_documents(({"solved": True})) + 1,
    }

@route("/")
def root():
    return static_file("index.html", root="./")


@route("/ax")
def root():
    return static_file("ax.mp3", root="./")



@route("/wn")
def root():
    return static_file("wn.mp3", root="./")


run(host="0.0.0.0", port=8000, server="gunicorn", workers=2)
app = default_app()

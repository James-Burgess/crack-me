import ujson as json
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
)
import redis

from worker import RedisQueue
from request_utils import interceptor

incrementor = RedisQueue('test')


def check_credentials(user, pw):
    incrementor.put(user)
    password = "abcd"
    print(pw)
    return pw == password


@route("/locked")
@interceptor(check_credentials)
def win():
    return static_file("win.html", root="./")


@route("/")
def root():
    return static_file("index.html", root="./")


@route("/ax")
def root():
    return static_file("ax.mp3", root="./")


run(host="0.0.0.0", port=8000, server="gunicorn", workers=12)

app = default_app()

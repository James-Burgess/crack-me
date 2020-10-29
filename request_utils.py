import re

from bottle import request, static_file

from user import get_or_create_user


def interceptor(check, realm="private"):
    def decorator(func):
        def wrapper(*a, **ka):
            ua = request.headers.get("User-Agent")
            browser = re.search(
                "chrome|safari|mozilla|edge|firefox", ua, re.IGNORECASE
            )
            password = request.query.get("pass")
            usr = request.query.get("user")
            hash = request.query.get("hash")
            user = get_or_create_user(usr, hash, browser, password)

            if user is None:
                if browser:
                    return static_file("index.html", root="./")
                return "please sign up online"

            if not password or not check(user, password):
                if browser:
                    return static_file("fail.html", root="./")
                return "access denied"

            print(f"found password {password}")
            return func(user, *a, **ka)
        return wrapper
    return decorator

import re

from bottle import request, static_file

from user import get_or_create_user


def interceptor(check, realm="private"):
    def decorator(func):
        def wrapper(*a, **ka):
            ua = request.headers.get("User-Agent")
            browser = re.search(
                "chrome|safari|mozilla|edge|firefox", ua, re.IGNORECASE
            ).group()

            user = get_or_create_user(
                request.query.get("user"), request.query.get("hash"), browser
            )
            if user is None:
                if browser:
                    return static_file("index.html", root="./")
                return "please sign up online"

            password = request.query.get("pass")
            if not password or not check(user, password):
                if browser:
                    return static_file("fail.html", root="./")
                return "access denied"

            print(f"found password {password}")
            return func(*a, **ka)
        return wrapper
    return decorator

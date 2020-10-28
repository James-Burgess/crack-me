from bottle import auth_basic, request, route, error, static_file, run, abort
from bottle import route, Response, run, HTTPError, request
import re

def interceptor(check, realm="private", text="Access denied"):
    def decorator(func):
        def wrapper(*a, **ka):
            print('erere')

            ua = request.headers.get('User-Agent')
            is_browser = re.search('chrome|safari|mozilla|edge|firefox', ua, re.IGNORECASE)

            user = get_or_create_user(request.query.get('user'), request.query.get('hash'), is_browser)

            if user is None:
                if is_browser:
                    return static_file('index.html', root='./')
                return "please sign up online"

            password = request.query.get('pass')
            print(f"pass{password}")
            if not password or not check(password, user):
                if is_browser:
                    return static_file('fail.html', root='./')
                Response.status = 401
                return "access denied"
            return func(*a, **ka)
        return wrapper

    return decorator


users = {}
hashes = []
def get_or_create_user(user, hash, browser):
    global users
    print(user, hash)
    stored_user = users.get(user)

    if hash and stored_user:
        if stored_user.get("hash") != hash:
            return None
        return user
    elif stored_user:
        return user
    elif not hash:
        return None
    elif hash in hashes:
        return None
    elif browser:
        hashes.append(hash)
        users[user] = {"hash": hash}
        return user
    else:
        return None


def check_credentials(pw, user):
    print(pw)
    username = "test"
    password = "test"
    return pw == password



@route('/locked')
@interceptor(check_credentials)
def win():
    return static_file('win.html', root='./')

@route('/')
def root():
    return static_file('index.html', root='./')

@route('/ax')
def root():
    return static_file('ax.mp3', root='./')


run(host='0.0.0.0', port=8080, debug=True)

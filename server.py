from bottle import auth_basic, request, route, error, static_file, run


from bottle import route, Response, run, HTTPError, request

auth_enabled = True


def custom_auth_basic(check, realm="private", text="Access denied"):
    ''' Callback decorator to require HTTP auth (basic).
        TODO: Add route(check_auth=...) parameter. '''
    def decorator(func):
        def wrapper(*a, **ka):
            print('erere')
            password = request.query['pass'] or None
            print(password)
            if password is None or not check(password):
                err = static_file('fail.html', root='./')
                # err.add_header('WWW-Authenticate', 'Basic realm="%s"' % realm)
                return err
            return func(*a, **ka)

        return wrapper

    return decorator


def check_credentials(pw):
    print(pw)
    username = "test"
    password = "test"
    return pw == password



@route('/locked')
@custom_auth_basic(check_credentials)
def win():
    return static_file('win.html', root='./')

@route('/')
def root():
    return static_file('index.html', root='./')

@route('/ax')
def root():
    return static_file('ax.mp3', root='./')

run(host='localhost', port=8080)

# @route('/')
# @auth_basic(is_authenticated_user)
# def hello():
#
#
# run(host='0.0.0.0', port=8080, debug=True)

from flask import session, after_this_request, request, make_response
from Crypto.Hash import SHA256
import random, time, os
from functools import wraps

static_value = os.environ.get("SECRET")
sha256 = SHA256.new()

# https://portswigger.net/web-security/csrf/tokens
# https://owasp.org/www-community/attacks/csrf
def gen_csrf():
    """Generates a sufficiently pseudorandom string to be used as a csrf token"""
    random.seed(str(time.time()).encode() + static_value.encode())
    sha256.update(random.randbytes(64))
    return sha256.digest().hex()
    

def check_csrf(view):
    """This decorator is used on routes that require anti-csrf protection (mostly HTTP POST)"""
    @wraps(view)
    def func(*args, **kwargs):
        # Otherwize generic decorator boilerplate
        resp = make_response()
        server_token = session.get("csrf_token")
        json_recv = request.get_json()
        if not "token" in json_recv:
            resp.status = "400"
            return resp
        @after_this_request
        def check(response):
            # If the tokens do not match, hijack the response and
            # return our one instead with a 401 Forbidden.
            # If they do match return the original response
            if not server_token == json_recv["token"]:
                resp.status = "401"
                return resp
            return response
        return view(*args, **kwargs)
    return func
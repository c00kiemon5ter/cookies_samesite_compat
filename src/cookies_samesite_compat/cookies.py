import http.cookies as _cookies
import types


_cookies.Morsel._reserved["samesite"] = "SameSite"


def parse(serialized_cookies):
    cookies_raw = (
        serialized_cookies
        if isinstance(serialized_cookies, str)
        else ";".join(serialized_cookies)
        if isinstance(serialized_cookies, types.Iterable)
        else ""
    )
    container = _cookies.SimpleCookie(cookies_raw)
    cookies = ((cookie.key, cookie) for name, cookie in container.items())
    return cookies


def create(key, value, properties=[]):
    props = properties or []
    cookie = _cookies.SimpleCookie({key: value})[key]
    for prop, value in props:
        cookie[prop] = value
    return (key, cookie)


def serialize(cookie, header=""):
    name, data = cookie
    value = data.output(header=header)
    return (name, value)

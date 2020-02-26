import copy

from . import cookies as Cookies


class CookiesSameSiteCompatMiddleware(object):
    def __init__(self, app, config={}):
        self.app = app
        self.primary_to_fallback = config.get("cookies_samesite_compat") or []

    def _customize_request(self, environ):
        old_to_new_names = [
            (fallback, primary)
            for entry in self.primary_to_fallback
            for primary, fallback in [entry]
        ]
        environ_new = customize_request(environ, old_to_new_names)
        return environ_new

    def _customize_response(self, headers):
        old_to_new_names = self.primary_to_fallback
        headers_new = customize_response(headers, old_to_new_names)
        return headers_new

    def __call__(self, environ, start_response):
        def customize_response(status, headers, exc_info=None):
            headers_customized = self._customize_response(headers)
            return start_response(status, headers_customized, exc_info)

        environ_customized = self._customize_request(environ)
        data = self.app(environ_customized, customize_response)
        return data


def customize_request(environ, old_to_new_names):
    cookies_from_env = dict(get_cookies_from_items(environ.items(), "HTTP_COOKIE"))
    cookies_created_from_fallbacks = create_new_cookies_from(
        cookies_from_env, old_to_new_names
    )
    cookies_all = (*cookies_from_env.items(), *cookies_created_from_fallbacks)
    cookies_raw = (
        data for cookie in cookies_all for name, data in [Cookies.serialize(cookie)]
    )

    # pack & mutate
    cookies_raw_value = ";".join(cookies_raw)
    environ["HTTP_COOKIE"] = cookies_raw_value

    return environ


def customize_response(headers, old_to_new_names):
    cookies_from_headers = dict(get_cookies_from_items(headers, "Set-Cookie"))
    cookies_created_from_primaries = create_new_cookies_from(
        cookies_from_headers, old_to_new_names, [("samesite", "")]
    )
    cookies_all = (*cookies_from_headers.items(), *cookies_created_from_primaries)
    cookies_raw = (
        data for cookie in cookies_all for name, data in [Cookies.serialize(cookie)]
    )

    # pack & mutate
    cookies_headers = (("Set-Cookie", data) for data in cookies_raw)
    headers_with_no_cookies = (
        (name, data)
        for entry in headers
        for name, data in [entry]
        if name != "Set-Cookie"
    )
    headers_all = (*headers_with_no_cookies, *cookies_headers)
    headers_new = list(headers_all)

    return headers_new


def get_cookies_from_items(items, key):
    cookies_raw = ";".join(
        data for entry in items for name, data in [entry] if name == key
    )
    cookies = Cookies.parse(cookies_raw)
    return cookies


def create_new_cookies_from(cookies, old_to_new_names, properties=[]):
    cookies_to_create = (
        (new_name, cookies[old_name])
        for entry in old_to_new_names
        for old_name, new_name in [entry]
        if new_name not in cookies
        if old_name in cookies
    )
    cookies_created = (
        Cookies.create(new_name, old_cookie.value, (*old_cookie.items(), *properties))
        for entry in cookies_to_create
        for new_name, old_cookie in [entry]
    )
    return cookies_created

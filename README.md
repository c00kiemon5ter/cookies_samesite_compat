## Cookies SameSite compatibility WSGI Middleware

This is a WSGI Middleware that given a configuration dictionary it will look
for the `cookies_samesite_compat` field that should hold a list of two-element
tuples that define two cookie names. The first name is the primary cookie name
and the second is the fallback cookie name. The primary cookie should be set by
the application with all needed attributes set, including the `SameSite`
attribute.

On creating the response, the fallback cookie is created based on the primary
cookie, but with the its own name and without the `SameSite` attributes. On
processing a request, if the primary cookie is not there, the fallback cookie
is looked up and used to create the primary cookie, even if the SameSite
attribute will not be set, so that the appication can only care about one
cookie name.


### Usage

```python
from cookies_samesite_compat import CookiesSameSiteCompatMiddleware


config = get_config()
response = CookiesSameSiteCompatMiddleware(
    WsgiApplication(config), config
)
return response
```

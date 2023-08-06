def cookieExpiryFormat(epochtime):
    return time.strftime("%a, %d-%b-%Y %T GMT", time.gmtime(epochtime))

def getCookieDict(environ):
    if "HTTP_COOKIE" in environ:
        return SimpleCookie(environ["HTTP_COOKIE"])
    else:
        return {}

def cookieError(name, value):
    return {"name": name, "value": value, "expires": time.time() + 10}

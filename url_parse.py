#!/usr/bin/env python3
"""url_parse: URL parser and builder (RFC 3986)."""
import re, sys

class URL:
    def __init__(self, scheme="", authority="", userinfo="", host="", port=None,
                 path="", query="", fragment=""):
        self.scheme = scheme; self.userinfo = userinfo; self.host = host
        self.port = port; self.path = path; self.query = query; self.fragment = fragment

    @property
    def authority(self):
        a = ""
        if self.userinfo: a += self.userinfo + "@"
        a += self.host
        if self.port is not None: a += f":{self.port}"
        return a

    def __str__(self):
        result = ""
        if self.scheme: result += self.scheme + "://"
        result += self.authority
        result += self.path
        if self.query: result += "?" + self.query
        if self.fragment: result += "#" + self.fragment
        return result

    def query_params(self):
        if not self.query: return {}
        params = {}
        for pair in self.query.split("&"):
            if "=" in pair:
                k, v = pair.split("=", 1)
                params[k] = v
            elif pair:
                params[pair] = ""
        return params

def parse(url_str):
    pattern = r'^(?:([a-zA-Z][a-zA-Z0-9+.-]*):)?(?://(?:([^@]*)@)?([^/:?#]*)(?::(\d+))?)?([^?#]*)(?:\?([^#]*))?(?:#(.*))?$'
    m = re.match(pattern, url_str)
    if not m: raise ValueError(f"Invalid URL: {url_str}")
    return URL(
        scheme=m.group(1) or "",
        userinfo=m.group(2) or "",
        host=m.group(3) or "",
        port=int(m.group(4)) if m.group(4) else None,
        path=m.group(5) or "",
        query=m.group(6) or "",
        fragment=m.group(7) or "",
    )

def percent_encode(s, safe=""):
    result = []
    for c in s:
        if c.isalnum() or c in "-._~" + safe:
            result.append(c)
        else:
            result.append(f"%{ord(c):02X}")
    return "".join(result)

def percent_decode(s):
    result = []
    i = 0
    while i < len(s):
        if s[i] == "%" and i + 2 < len(s):
            result.append(chr(int(s[i+1:i+3], 16)))
            i += 3
        else:
            result.append(s[i]); i += 1
    return "".join(result)

def test():
    u = parse("https://user:pass@example.com:8080/path/to?q=1&r=2#frag")
    assert u.scheme == "https"
    assert u.userinfo == "user:pass"
    assert u.host == "example.com"
    assert u.port == 8080
    assert u.path == "/path/to"
    assert u.query == "q=1&r=2"
    assert u.fragment == "frag"
    assert u.query_params() == {"q": "1", "r": "2"}
    # Roundtrip
    assert str(u) == "https://user:pass@example.com:8080/path/to?q=1&r=2#frag"
    # Simple
    u2 = parse("http://localhost/")
    assert u2.host == "localhost"
    assert u2.port is None
    # Percent encoding
    assert percent_encode("hello world") == "hello%20world"
    assert percent_decode("hello%20world") == "hello world"
    assert percent_encode("/path", safe="/") == "/path"
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: url_parse.py test")

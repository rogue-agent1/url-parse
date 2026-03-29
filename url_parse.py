#!/usr/bin/env python3
"""url_parse - URL parser and builder (RFC 3986 subset)."""
import sys, re

class URL:
    def __init__(self, scheme="", host="", port=None, path="/", query="", fragment="", userinfo=""):
        self.scheme, self.host, self.port = scheme, host, port
        self.path, self.query, self.fragment = path, query, fragment
        self.userinfo = userinfo
    def query_params(self):
        if not self.query: return {}
        params = {}
        for part in self.query.split("&"):
            if "=" in part:
                k, v = part.split("=", 1)
                params[k] = v
            else:
                params[part] = ""
        return params
    def __str__(self):
        s = f"{self.scheme}://" if self.scheme else ""
        if self.userinfo: s += f"{self.userinfo}@"
        s += self.host
        if self.port: s += f":{self.port}"
        s += self.path
        if self.query: s += f"?{self.query}"
        if self.fragment: s += f"#{self.fragment}"
        return s

def parse_url(raw):
    m = re.match(r"(?:(\w+)://)?(?:([^@]+)@)?([^/:?#]+)(?::(\d+))?(\/[^?#]*)?(?:\?([^#]*))?(?:#(.*))?", raw)
    if not m: return None
    scheme, userinfo, host, port, path, query, fragment = m.groups()
    return URL(scheme or "", host or "", int(port) if port else None,
               path or "/", query or "", fragment or "", userinfo or "")

def test():
    u = parse_url("https://user:pass@example.com:8080/path?q=1&r=2#frag")
    assert u.scheme == "https"
    assert u.userinfo == "user:pass"
    assert u.host == "example.com"
    assert u.port == 8080
    assert u.path == "/path"
    assert u.query_params() == {"q": "1", "r": "2"}
    assert u.fragment == "frag"
    u2 = parse_url("http://localhost/api")
    assert u2.host == "localhost" and u2.path == "/api" and u2.port is None
    assert "localhost/api" in str(u2)
    print("url_parse: all tests passed")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("Usage: url_parse.py --test")

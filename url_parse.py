#!/usr/bin/env python3
"""url_parse - URL parser, builder, and normalizer."""
import sys, re

class URL:
    def __init__(self, scheme="", host="", port=None, path="/", query=None, fragment="", userinfo=""):
        self.scheme = scheme
        self.host = host
        self.port = port
        self.path = path
        self.query = query or {}
        self.fragment = fragment
        self.userinfo = userinfo

    @staticmethod
    def parse(url_str):
        m = re.match(r'^(?:([a-z][a-z0-9+.-]*):)?//(?:([^@]+)@)?([^:/?#]+)(?::(\d+))?([^?#]*)(?:\?([^#]*))?(?:#(.*))?$', url_str, re.I)
        if not m:
            return URL(path=url_str)
        scheme, userinfo, host, port, path, qs, frag = m.groups()
        query = {}
        if qs:
            for pair in qs.split("&"):
                if "=" in pair:
                    k, v = pair.split("=", 1)
                    query[k] = v
                else:
                    query[pair] = ""
        return URL(scheme=scheme or "", host=host or "", port=int(port) if port else None,
                   path=path or "/", query=query, fragment=frag or "", userinfo=userinfo or "")

    def to_string(self):
        s = ""
        if self.scheme:
            s += f"{self.scheme}://"
        if self.userinfo:
            s += f"{self.userinfo}@"
        s += self.host
        if self.port:
            s += f":{self.port}"
        s += self.path or "/"
        if self.query:
            qs = "&".join(f"{k}={v}" if v else k for k, v in self.query.items())
            s += f"?{qs}"
        if self.fragment:
            s += f"#{self.fragment}"
        return s

    def with_query(self, key, value):
        q = dict(self.query)
        q[key] = value
        return URL(self.scheme, self.host, self.port, self.path, q, self.fragment, self.userinfo)

    def normalize(self):
        scheme = self.scheme.lower()
        host = self.host.lower()
        path = self.path or "/"
        port = self.port
        if (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
            port = None
        return URL(scheme, host, port, path, self.query, self.fragment, self.userinfo)

def test():
    u = URL.parse("https://user:pass@example.com:8080/path?key=val&foo=bar#section")
    assert u.scheme == "https"
    assert u.host == "example.com"
    assert u.port == 8080
    assert u.path == "/path"
    assert u.query == {"key": "val", "foo": "bar"}
    assert u.fragment == "section"
    assert u.userinfo == "user:pass"
    simple = URL.parse("http://example.com")
    assert simple.scheme == "http"
    assert simple.host == "example.com"
    u2 = simple.with_query("page", "1")
    assert u2.query["page"] == "1"
    norm = URL.parse("HTTP://Example.COM:80/Path").normalize()
    assert norm.scheme == "http"
    assert norm.host == "example.com"
    assert norm.port is None
    s = URL.parse("https://api.example.com/v1/users?limit=10").to_string()
    assert "https://api.example.com/v1/users" in s
    assert "limit=10" in s
    print("All tests passed!")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("url_parse: URL parser. Use --test")

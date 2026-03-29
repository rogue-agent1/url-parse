#!/usr/bin/env python3
"""URL parser and builder. Zero dependencies."""
import sys

class URL:
    def __init__(self, url=""):
        self.scheme = ""; self.host = ""; self.port = 0
        self.path = ""; self.query = {}; self.fragment = ""
        self.username = ""; self.password = ""
        if url: self._parse(url)

    def _parse(self, url):
        rest = url
        if "://" in rest:
            self.scheme, rest = rest.split("://", 1)
        if "#" in rest:
            rest, self.fragment = rest.rsplit("#", 1)
        if "?" in rest:
            rest, qs = rest.split("?", 1)
            for pair in qs.split("&"):
                if "=" in pair:
                    k, v = pair.split("=", 1)
                    self.query[_decode(k)] = _decode(v)
                else:
                    self.query[_decode(pair)] = ""
        if "/" in rest:
            hostpart, self.path = rest.split("/", 1)
            self.path = "/" + self.path
        else:
            hostpart = rest; self.path = "/"
        if "@" in hostpart:
            userinfo, hostpart = hostpart.rsplit("@", 1)
            if ":" in userinfo:
                self.username, self.password = userinfo.split(":", 1)
            else:
                self.username = userinfo
        if ":" in hostpart and hostpart.count(":") == 1:
            self.host, port_s = hostpart.rsplit(":", 1)
            try: self.port = int(port_s)
            except: self.host = hostpart
        else:
            self.host = hostpart

    def build(self):
        url = ""
        if self.scheme: url += f"{self.scheme}://"
        if self.username:
            url += self.username
            if self.password: url += f":{self.password}"
            url += "@"
        url += self.host
        if self.port: url += f":{self.port}"
        url += self.path
        if self.query:
            url += "?" + "&".join(f"{_encode(k)}={_encode(v)}" for k, v in self.query.items())
        if self.fragment: url += f"#{self.fragment}"
        return url

    def __repr__(self):
        return self.build()

    def with_query(self, **kwargs):
        u = URL(self.build())
        u.query.update(kwargs)
        return u

    def with_path(self, path):
        u = URL(self.build())
        u.path = path
        return u

def _encode(s):
    safe = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~")
    return "".join(c if c in safe else f"%{ord(c):02X}" for c in str(s))

def _decode(s):
    result = []; i = 0
    while i < len(s):
        if s[i] == "%" and i+2 < len(s):
            result.append(chr(int(s[i+1:i+3], 16))); i += 3
        elif s[i] == "+": result.append(" "); i += 1
        else: result.append(s[i]); i += 1
    return "".join(result)

def encode(s): return _encode(s)
def decode(s): return _decode(s)

if __name__ == "__main__":
    u = URL(sys.argv[1] if len(sys.argv) > 1 else "https://user:pass@example.com:8080/path?q=hello&lang=en#section")
    print(f"scheme: {u.scheme}")
    print(f"host: {u.host}")
    print(f"port: {u.port}")
    print(f"path: {u.path}")
    print(f"query: {u.query}")
    print(f"fragment: {u.fragment}")
    print(f"rebuilt: {u.build()}")

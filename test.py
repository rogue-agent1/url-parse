from url_parse import URL, encode, decode
u = URL("https://user:pass@example.com:8080/path?q=hello#frag")
assert u.scheme == "https"
assert u.host == "example.com"
assert u.port == 8080
assert u.path == "/path"
assert u.query["q"] == "hello"
assert u.fragment == "frag"
assert u.username == "user"
u2 = u.with_query(lang="en")
assert "lang" in u2.query
assert encode("hello world") == "hello%20world"
assert decode("hello%20world") == "hello world"
print("URL parse tests passed")
s = "Hi, {name}!"
data = {
    "name": "Bob"
}
s = s.format(**data)
print(s)
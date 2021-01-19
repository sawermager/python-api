import requests


#r = requests.get('http://requestbin.net/r/1jib4041')

r = requests.get('https://reqres.in/api/users?page=2')

print(r)
a=print(r.json())
print(type(a))
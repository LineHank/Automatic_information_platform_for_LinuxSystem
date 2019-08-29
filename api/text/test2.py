import requests, json

data = {
    'id': 1,
    'name': 'lily',
    'age': 11,
    'birthplace': 'san',
    'grade': 123
}
url = 'http://localhost:5000/add/stuent/'

r = requests.post(url, data=json.dumps(data))
print(r.json())
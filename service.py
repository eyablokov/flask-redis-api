import json
from flask import Flask, Response, request
import redis
from datetime import datetime

app = Flask(__name__)
app.debug = True

db = redis.Redis('localhost')

def check_username(u):
    if not u.isalpha():
        raise ValueError('Username must contain letters only.')
    else:
        return 0

def check_birthday_format(b):
    try:
        datetime.strptime(b, '%Y-%m-%d')
        return 0
    except ValueError:
        raise ValueError('Date of Birth has to be in YYYY-MM-DD format.')

@app.route('/')
def hello():
    return 'Hi.'

@app.route('/hello/<username>', methods=['GET'])
def get_username_data(username):
    check_username(username)
    resp = {}
    birthday = db.get(username).decode().replace("\'", "\"")
    today = datetime.now()
    for date in birthday.keys():
        if date.date() < today.date():
            resp = '{"message": "Hello, {}! Happy birthday!"}'.format(username)
        else:
            num_days = max(date, today).days
            resp = '{"message": "Hello, {}! Your birthday is in {} days."}'.format(username, num_days)
    final = json.loads(resp)
    return Response(json.dumps(final), status=200, mimetype='application/json')

@app.route('/hello/<username>', methods=['PUT'])
def map_username_data(username):
    check_username(username)
    data = request.get_json(force=True)
    for key in data.keys():
        check_birthday_format(data[key])
    if username:
        db.set(username, data)
    return Response(status=204)

@app.route('/clear', methods=['GET'])
def clear_data():
    db.flushall()
    return 'All data cleared.'

if __name__ == "__main__":
    app.run()

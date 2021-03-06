import datetime
import json
from flask import Flask, Response, request
import redis

app = Flask(__name__)
app.debug = True

db = redis.Redis('redis')

def check_username(u):
    if not u.isalpha():
        raise ValueError('Username must contain letters only.')
    return 0

def check_birthday_format(b):
    try:
        datetime.datetime.strptime(b, '%Y-%m-%d')
        return 0
    except ValueError:
        raise ValueError('Date of Birth has to be in YYYY-MM-DD format.')

@app.route('/')
def hello():
    return 'Hi.'

@app.route('/hello/<username>', methods=['GET'])
def get_username_data(username):
    check_username(username)
    birthday = db.get(username).decode().replace("\'", "\"")
    today = datetime.date.today()
    date_dict = json.loads(birthday)
    for birth in date_dict.values():
        datetime_birth = datetime.datetime.strptime(birth, '%Y-%m-%d').date()
        if datetime_birth == today:
            line = '{"message":"Hello, '+ username + '! Happy birthday!" }'
            return Response(json.loads(line), status=200)
        if (today.month == datetime_birth.month and today.day >= datetime_birth.day or today.month > datetime_birth.month):
            nextBirthdayYear = today.year + 1
        else:
            nextBirthdayYear = today.year
        nextBirthday = datetime.date(nextBirthdayYear, datetime_birth.month, datetime_birth.day)
        diff = nextBirthday - today
        line = '{"message":"Hello, ' + username + '! Your birthday is in ' + str(diff.days) + ' day(s)"}'
        return Response(json.loads(line), status=200)

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

import json
from flask import Flask, Response, request
import redis
import sys

app = Flask(__name__)
app.debug = True

db = redis.Redis('localhost')

@app.route('/')
def hello():
    return 'Hi.'

@app.route('/hello/<username>', methods=['GET'])
def get_username_data(username):
    if username.isalpha() is False:
        sys.stderr.write('Username must contain letters only.')
        sys.exit(1)
    resp = {}
    output = db.get(username)
    birthday = output.decode().replace("\'", "\"")
    resp = json.loads(birthday)
    return Response(json.dumps(resp), status=200, mimetype='application/json')

@app.route('/hello/<username>', methods=['PUT'])
def map_username_data(username):
    if username.isalpha() is False:
        print('Username must contain letters only.')
        sys.exit(1)
    data = request.get_json(force=True)
    if username:
        db.set(username, data)
    return Response(status=204)

@app.route('/clear', methods=['GET'])
def clear_data():
    db.flushall()
    return 'All data cleared.'

if __name__ == "__main__":
    app.run()

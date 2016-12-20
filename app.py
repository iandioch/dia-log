import pendulum
import json
import sys
from auth import Auth
from flask import Flask, request

app = Flask(__name__)
auth = None

config = {}

def check_auth(user, password):
    valid = auth.check_user_pass(user, password)
    if valid:
        print('User %s authenticated successfully.' % user)
    else:
        print('User %s did not authenticate succesfully!' % user)
    return valid

@app.route("/blood/add/", methods=['POST'])
def add_blood():
    user = request.form['user']
    password = request.form['pass']
    if not check_auth(user, password):
        return 'not ok'
    date = pendulum.parse(request.form['date'])
    print(date)
    mmol = request.form['mmol']
    return 'ok'

def load_config_file():
    config_file = 'config.json'
    if (len(sys.argv) > 1):
        config_file = ' '.join(sys.argv[1:])
    print ('Using %s as config file' % config_file)
    tmp_config = {}
    with open(config_file, 'r') as f:
        tmp_config = json.load(f)
    return tmp_config

if __name__ == '__main__':
    config = load_config_file()
    auth = Auth(debug=config['debug'])
    auth.load_password_file(config['password_file'])
    app.run(host=config['host'], port=config['port'])

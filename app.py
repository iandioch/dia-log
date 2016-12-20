import pendulum
import json
import sys
from flask import Flask, request
app = Flask(__name__)

config = {}

@app.route("/blood/add/", methods=['POST'])
def add_blood():
    user = request.form['user']
    password = request.form['pass']
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
    app.run(host=config['host'], port=config['port'])

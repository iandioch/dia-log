import json
import os
import pendulum
import sys
from auth import Auth
from flask import Flask, request, send_from_directory

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


@app.route("/api/blood/add/", methods=['POST'])
def add_blood():
    user = request.form['user']
    password = request.form['pass']
    if not check_auth(user, password):
        return 'not ok'
    date = pendulum.parse(request.form['date'])
    mmol = float(request.form['mmol'])
    outdir = (config['blood_dir'] + '/' + user)
    outfile = outdir + '/' + date
    print ('Writing %s\'s blood level to "%s"' %
            (user, outfile))
    os.makedirs(outdir)
    with open(outdir + '/' + date, 'w') as f:
        f.write(mmol)
        f.write('\n')
    return 'ok'


@app.route('/api/admin/add_user/', methods=['POST'])
def add_user():
    old_user = request.form['user']
    old_pass = request.form['pass']
    if not check_auth(old_user, old_pass):
        return 'not ok'
    new_user = request.form['new_user']
    new_pass = request.form['new_pass']
    auth.add_user_pass(new_user, new_pass)
    print ('New user %s added successfully by %s' % (new_user, old_user))
    auth.save_password_file(config['password_file'])
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

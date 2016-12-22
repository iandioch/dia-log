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


def load_list_of_blood_files(user):
    return os.listdir(config['blood_dir'] + '/' + user)


def load_blood_file(user, date):
    with open(config['blood_dir'] + '/' + user + '/' + date, 'r') as f:
        return float(f.readline())


@app.route("/blood/add/", methods=['POST'])
def add_blood():
    user = request.form['user']
    password = request.form['pass']
    if not check_auth(user, password):
        return 'not ok'
    raw_date = request.form['date']
    date = pendulum.parse(raw_date)
    print ('raw: "%s", parsed date: "%s"' %
            (raw_date, date))
    mmol = float(request.form['mmol'])
    outdir = (config['blood_dir'] + '/' + user)
    outfile = outdir + '/' + str(date)
    print ('Writing %s\'s blood level to "%s"' %
            (user, outfile))
    try:
        os.makedirs(outdir)
    except OSError as e:
        # dir already exists
        print(e)
    with open(outfile, 'w') as f:
        f.write(str(mmol))
        f.write('\n')
    return 'ok'


"""
Get data about a single reading.
Takes parameters `user`, `pass`, and `n`,
where `user` and `pass` are login details,
and `n` says which reading you want (ie.
`n` of 0 is the most recent reading, `n` of
23 is the 24th most recent reading).
"""
@app.route("/blood/get/", methods=['POST'])
def get_blood():
    user = request.form['user']
    password = request.form['pass']
    if not check_auth(user, password):
        return 'not ok'
    n = 0
    if 'n' in request.form:
        n = int(request.form['n'])
    files = load_list_of_blood_files(user)
    if 0 <= n < len(files):
        date = files[n]
        return json.dumps({
            'date': date,
            'mmol': load_blood_file(user, date)
        })
    return 'not ok'


@app.route('/admin/add_user/', methods=['POST'])
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

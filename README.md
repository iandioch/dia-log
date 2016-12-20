# dia-log

A JSON-based REST server (with some authentification) to allow a number of users (or just one; your server, your rules) to upload their blood glucose readings to a server, for the purposes of backup, aggregation, or whatever else your weakened pancreas desires.

All numbers are expected to be in `mmol/L`.

# Setup

Requires python2 (might work with python3, I haven't tried xo). Run `pip install -r requirements.txt` to install the dependencies.

The first time you run the server (with `python app.py`), you should run it with `debug` set to `true` in `config.json`. This will let you add a new user account, with something like the following:

`curl -XPOST -d 'user=default&pass=CHECK_CONFIG_DOT_JS&new_user=NEW_USER&new_pass=NEW_PASS'`, where the `user` and `pass` fields are whatever are set in your config file (by default, `user` is `default` and `pass` is `change_me_ffs`).


You should run the server with `debug` set to `false` from then on.

Passwords are `bcrypt`-ed, and kept in a json file of your choosing. You can pass the config file location as a command line argument to `app.py`, eg. run `python app.py config.json`.

# Contributing

PRs and issues are encouraged.

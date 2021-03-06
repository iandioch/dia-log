import json
from passlib.hash import bcrypt

class Auth:
    def __init__(self, debug=False):
        """Initialise the Auth object. If `debug` is set,
        then plaintext passwords will be matched as well
        as hashed ones."""
        self.db = {}
        self.debug = debug

    def _encrypt(self, data):
        return bcrypt.using(rounds=12).hash(data)

    def load_password_file(self, file_loc):
        with open(file_loc, 'r') as f:
            self.db = json.load(f)

    def check_user_pass(self, user, password):
        """Returns True if the given user & pass is valid,
        and False otherwise."""
        if user not in self.db:
            return False
        if self.debug:
            return self.db[user] == password or \
                    bcrypt.verify(password, self.db[user]) 
        try:
            return bcrypt.verify(password, self.db[user]) 
        except ValueError:
            # happens when password is in plaintext, for debug
            # mode
            return False

    def add_user_pass(self, user, password):
        hashed_pw = self._encrypt(password)
        self.db[user] = hashed_pw

    def save_password_file(self, file_loc):
        with open(file_loc, 'w') as f:
            json.dump(self.db, f)

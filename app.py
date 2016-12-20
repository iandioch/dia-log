from flask import Flask
app = Flask(__name__)

@app.route("/blood/add/")
def add_blood():
    pass

if __name__ == '__main__':
    app.run(host='localhost', port=7886)

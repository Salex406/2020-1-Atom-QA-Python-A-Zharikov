import threading
from flask import Flask, abort, request, jsonify


app = Flask(__name__)
users = dict()
host = '127.0.0.1'
port = 5000


def run_mock():
    server = threading.Thread(target=app.run, kwargs={'host': host, 'port': port})
    server.start()
    return server


def shutdown_mock():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/user/<user_id>')
def get_user_by_id(user_id: int):
    user = users.get(int(user_id), None)
    if user:
        return user
    else:
        abort(404)


@app.route('/add_user', methods=['POST'])
def add_user():
    user_n = len(users)
    temp = {"name": request.form['username'], "surname": request.form['surname']}
    users.update({user_n: temp})
    return jsonify(success=True)


@app.route('/test', methods=['GET'])
def test():
    return jsonify(success=True)


@app.route('/shutdown')
def shutdown():
    shutdown_mock()
    return jsonify(success=True)


if __name__ == '__main__':
    run_mock()

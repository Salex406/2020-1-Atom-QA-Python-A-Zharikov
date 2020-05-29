import threading
from flask import Flask, abort, request, jsonify, Response
import json


app = Flask(__name__)
users = {"qa_test": "12345"}
host = '0.0.0.0'
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

@app.route('/add_user', methods=['POST'])
def add_user_network():
    temp = {request.form['username']: request.form['id']}
    users.update(temp)
    return jsonify(success=True)

@app.route('/test', methods=['GET'])
def test():
    return jsonify(success=True)

@app.route('/vk_id/<username>', methods=['GET'])
def vk_id(username: str):
    try:
        id = users.get(username)
        ans = {"vk_id": id}
        js = json.dumps(ans)
        return Response(js, status=200, mimetype='application/json')
    except KeyError:     
        ans = {}
        js = json.dumps(ans)
        return Response(js, status=404, mimetype='application/json')

@app.route('/shutdown')
def shutdown():
    shutdown_mock()
    return jsonify(success=True)

if __name__ == '__main__':
    run_mock()

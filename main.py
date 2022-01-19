from server_controller import ServerController

from flask import Flask
from flask import jsonify, request
from flask_cors import CORS
from task import Task

server_controller = ServerController()

app = Flask(__name__)
CORS(app)

@app.route("/monitor")
def monitor():
    return jsonify(server_controller.monitor())


@app.route("/configure", methods = ["POST"])
def configure():
    vm_number = request.get_json()["vm_number"]
    return jsonify(server_controller.configure(vm_number))

@app.route("/send", methods = ["POST"])
def send_request():
    tasks = request.get_json()["tasks"]
    tasks_obj = [ Task(task["duration"]) for task in tasks]
    return jsonify(server_controller.send_request(tasks_obj))
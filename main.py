from crypt import methods
import json
import time
import random
from server_controller import ServerController
from task import Task
from request import Request
from controller import Controller
from loadBalancer import LoadBalancer
from virtualMachine import VirtualMachine
from virtualMachineDiagnosticService import VirtualMachineDiagnosticService as VMDiagService

from flask import Flask
from flask import jsonify, request
from flask_cors import CORS

server_controller: ServerController = ServerController()

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
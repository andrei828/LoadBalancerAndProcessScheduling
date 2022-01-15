import time
from task import Task
from request import Request
from controller import Controller
from loadBalancer import LoadBalancer
from virtualMachine import VirtualMachine

loadBalancer = LoadBalancer([VirtualMachine(), VirtualMachine()]).initialize()
controller = Controller().initialize()
loadBalancer.setController(controller)
controller.setLoadBalancer(loadBalancer)

for i in range(100):
    controller.sendRequest(Request([Task(43)]))

for i in range(100):
    print("Other tasks on main thread")

loadBalancer.stop()
controller.stop()
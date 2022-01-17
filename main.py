import time
from task import Task
from request import Request
from controller import Controller
from loadBalancer import LoadBalancer
from virtualMachine import VirtualMachine

# register services
virtualMachines = [VirtualMachine().initialize() for _ in range(3)]
loadBalancer = LoadBalancer(virtualMachines).initialize()
controller = Controller().initialize()
loadBalancer.setController(controller)
controller.setLoadBalancer(loadBalancer)

# send requests
for i in range(100):
    controller.receiveRequest(Request([Task(43)]))

# do other stuff on main thread
for i in range(100):
    print("Other tasks on main thread")

# stop the services
loadBalancer.stop()
controller.stop()
for virtualMachine in virtualMachines:
    virtualMachine.stop()
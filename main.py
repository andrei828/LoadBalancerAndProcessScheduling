import time
import random
from task import Task
from request import Request
from controller import Controller
from loadBalancer import LoadBalancer
from virtualMachine import VirtualMachine
from virtualMachineDiagnosticService import VirtualMachineDiagnosticService as VMDiagService

# register services
virtualMachines = [VirtualMachine().initialize() for _ in range(3)]
vmDiagService = VMDiagService(virtualMachines).initialize()
loadBalancer = LoadBalancer(virtualMachines).initialize()
controller = Controller().initialize()
loadBalancer.setController(controller)
controller.setLoadBalancer(loadBalancer)

# send requests
for i in range(100):
    controller.receiveRequest(Request([Task(random.randint(1, 50)) for _ in range(random.randint(1, 5))]))

# do other stuff on main thread
time.sleep(10)

# stop the services
vmDiagService.stop()
loadBalancer.stop()
controller.stop()
for virtualMachine in virtualMachines:
    virtualMachine.stop()
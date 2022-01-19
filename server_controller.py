from typing import List
from task import Task
from request import Request
from controller import Controller
from loadBalancer import LoadBalancer
from virtualMachine import VirtualMachine
from virtualMachineDiagnosticService import VirtualMachineDiagnosticService as VMDiagService

class ServerController:
  virtualMachines: List[VirtualMachine] = []
  vmDiagService: VMDiagService = None
  loadBalancer: LoadBalancer = None
  controller: Controller = None

  def configure(self, vm_number):
    if self.controller is not None:
      self._stop_services()
    
    self.virtualMachines = [VirtualMachine().initialize() for _ in range(vm_number)]
    self.vmDiagService = VMDiagService(self.virtualMachines).initialize()
    self.loadBalancer = LoadBalancer(self.virtualMachines).initialize()
    self.controller = Controller().initialize()
    self.loadBalancer.setController(self.controller)
    self.controller.setLoadBalancer(self.loadBalancer)
    return self.vmDiagService.queryVirtualMachinesState()


  def _stop_services(self):
    self.vmDiagService.stop()
    self.loadBalancer.stop()
    self.controller.stop()
    for virtualMachine in self.virtualMachines:
        virtualMachine.stop()

  def monitor(self):
    if self.controller is None:
      return None
    return self.vmDiagService.queryVirtualMachinesState()

  def send_request(self, tasks: List[Task]):
    self.controller.receiveRequest(Request(tasks))
    return self.vmDiagService.queryVirtualMachinesState()
  
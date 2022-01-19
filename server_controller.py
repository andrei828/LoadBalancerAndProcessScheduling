import re
from typing import List
from logger import Logger
from logging_level import LoggingLevel
from task import Task
from request import Request
from controller import Controller
from loadBalancer import LoadBalancer
from util import flatten
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

  def get_logs(self, level = LoggingLevel.INFO):
    if self.controller is None:
      return []
    controller_logs = ServerController._parse_log(self.controller._logger, level)
    loadBalancer_logs = ServerController._parse_log(self.loadBalancer._logger, level)
    vm_logs = flatten([ ServerController._parse_log(vm._logger, level) for vm in self.virtualMachines ])
    return sorted(flatten([controller_logs, loadBalancer_logs, vm_logs]), key=lambda l: l['timestamp'])

  def _parse_log(logger_instance: Logger, level: LoggingLevel):
    logs = logger_instance.read_logs()
    logs_arr = logs.split('\n')
    p = re.compile('\[(?P<level>[^\[\]]*)\] \[(?P<timestamp>[^\[\]]*)\] (?P<content>.*)')

    parsed_arr = []
    who = logger_instance.file_name.split('.')[0]
    for log in logs_arr:
      m = p.match(log)
      if m is not None:
        m_dict = m.groupdict()
        m_dict["from"] = who
        parsed_arr.append(m_dict)

    return parsed_arr

  
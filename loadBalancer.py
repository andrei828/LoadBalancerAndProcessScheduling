from __future__ import annotations
from virtualMachine import VirtualMachine
from controller import Controller
from datetime import datetime
from threading import Thread
from typing import List
import threading, queue
import random
import time

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller import Controller

class LoadBalancer(Thread):
    
    def __init__(self, virtualMachines: List[VirtualMachine] = None):
        Thread.__init__(self)
        self._killed = False
        self._virtualMachines = virtualMachines
        self._logger = open(f'logs/LoadBalancer.log', 'a')

    def initialize(self) -> LoadBalancer:
        self._virtualMachinesDictionary = {}
        for virtualMachine in self._virtualMachines:
            virtualMachine.setLoadBalancer(self)
            self._virtualMachinesDictionary[virtualMachine] = virtualMachine.runningPercentage

        self._printLog(f'Starting Load Balancer...')
        self.start()
        return self
    
    def stop(self):
        self._killed = True
        self._printLog(f'Stopping Load Balancer and all associated VMs...')
        for virtualMachine in self._virtualMachines:
            virtualMachine.stop()
    
    def setController(self, controller: Controller):
        self._controller = controller
        for virtualMachine in self._virtualMachines:
            virtualMachine.setController(controller)

    def receiveRequest(self, request: Request):
        print('Received request from controller')
        self._printLog(f'Received request [{request.name}] with {len(request.tasks)} Tasks.')
        vm = self._chooseVirtualMachine(request)
        self._respondToController(request, vm)
    
    def run(self):
        while True:
            self._pingVirtualMachines()
            time.sleep(1)
            if self._killed == True:
                break
        self._printLog(f'Load Balancer stopped.')
    
    def _chooseVirtualMachine(self, item: Request) -> VirtualMachine:
        print(f'Querying VMs for the best match...')
        self._printLog(f'Querying VMs for the best match...')

        # TODO: implement the algorithm for choosing VMs
        vm = self._virtualMachines[random.randint(0, len(self._virtualMachines) - 1)]
        
        print(f'Found VM: {vm.name}.')
        self._printLog(f'Virtual Machine [{vm.name}] has been chosen.')
        return vm

    def _respondToController(self, request: Request, virtualMachine: VirtualMachine):
        print(f'Responding to controller that Virtual Machine [{virtualMachine.name}] is available for request [{request.name}]')
        self._controller.receiveLoadBalancerDecision(request, virtualMachine)
    
    def _pingVirtualMachines(self):
        self._printLog(f'Pinging Virtual Machines to check their health and load.')
        # TODO: find a thread safe solution 
        for virtualMachine in self._virtualMachines:
            self._virtualMachinesDictionary[virtualMachine] = virtualMachine.runningPercentage
    
    def _printLog(self, content: str):
        self._logger.write(f'[{datetime.now()}] {content}\n')

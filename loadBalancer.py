from __future__ import annotations
from logger import Logger
from request import Request
from threading import Thread
from controller import Controller
from logging_level import LoggingLevel
from virtualMachine import VirtualMachine

from datetime import datetime
from functools import reduce
from typing import List
import threading, queue
import random
import time
import copy

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller import Controller

class LoadBalancer(Thread):
    
    def __init__(self, virtualMachines: List[VirtualMachine] = None):
        Thread.__init__(self)
        self._killed = False
        self._virtualMachines = virtualMachines
        self._logger = Logger('LoadBalancer.log')

    def initialize(self) -> LoadBalancer:
        self._virtualMachinesDictionary = {}
        for virtualMachine in self._virtualMachines:
            virtualMachine.setLoadBalancer(self)
            self._virtualMachinesDictionary[virtualMachine] = 0

        self._logger.log(f'Starting Load Balancer...')
        self.start()
        return self
    
    def stop(self):
        self._killed = True
        self._logger.log(f'Stopping Load Balancer and all associated VMs...')
        for virtualMachine in self._virtualMachines:
            virtualMachine.stop()
    
    def setController(self, controller: Controller):
        self._controller = controller
        for virtualMachine in self._virtualMachines:
            virtualMachine.setController(controller)

    def receiveRequest(self, request: Request):
        print('Received request from controller')
        self._logger.log(f'Received request [{request.name}] with {len(request.tasks)} Tasks.')
        vm = self._chooseVirtualMachine(request)
        self._respondToController(request, vm)
    
    def run(self):
        while True:
            self._pingVirtualMachines()
            time.sleep(1)
            if self._killed == True:
                break
        self._logger.log(f'Load Balancer stopped.')
    
    def _chooseVirtualMachine(self, item: Request) -> VirtualMachine:
        print(f'Querying VMs for the best match...')
        self._pingVirtualMachines()
        self._logger.log(f'Querying VMs for the best match...')
        vm = min(self._virtualMachinesDictionary, key=self._virtualMachinesDictionary.get)
        print(f'Found VM: {vm.name}.')
        self._logger.log(f'Virtual Machine [{vm.name}] has been chosen.')
        return vm

    def _respondToController(self, request: Request, virtualMachine: VirtualMachine):
        print(f'Responding to controller that Virtual Machine [{virtualMachine.name}] is available for request [{request.name}]')
        self._controller.receiveLoadBalancerDecision(request, virtualMachine)

    def _pingVirtualMachines(self):
        self._logger.log(f'Pinging Virtual Machines to check their health and load.', LoggingLevel.VERBOSE)
        virtualMachinesState = {}
        for virtualMachine in self._virtualMachines:
            self._logger.log(f'Locking Virtual Machine [{virtualMachine.name}]...', LoggingLevel.VERBOSE)
            virtualMachine.lockThread()

            currentLoad = copy.deepcopy(virtualMachine.getCurrentLoad())
            if virtualMachine.runningRequest:
                currentLoad.append(copy.deepcopy(virtualMachine.runningRequest))

            totalDurationForVm = 0
            for request in currentLoad:
                totalDurationForVm += reduce(lambda accumulator, task: accumulator + task.duration, request.tasks, 0)
            
            runningPercentage = round(totalDurationForVm / 1000, 3)
            self._virtualMachinesDictionary[virtualMachine] = runningPercentage
            
            self._logger.log(f'Releasing Virtual Machine [{virtualMachine.name}]...', LoggingLevel.VERBOSE)
            virtualMachine.unlockThread()
    

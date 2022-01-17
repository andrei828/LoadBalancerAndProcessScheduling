from __future__ import annotations
from virtualMachine import VirtualMachine
from controller import Controller
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
        self._queue = queue.Queue()
        self._virtualMachines = virtualMachines
    
    def __del__(self):
        # wait for tasks to finish
        self._queue.join()
    
    def initialize(self) -> LoadBalancer:
        self._virtualMachinesDictionary = {}
        for virtualMachine in self._virtualMachines:
            virtualMachine.setLoadBalancer(self)
            self._virtualMachinesDictionary[virtualMachine] = virtualMachine.runningPercentage

        self.start()
        return self
    
    def stop(self):
        self._killed = True
        for virtualMachine in self._virtualMachines:
            virtualMachine.stop()
    
    def setController(self, controller: Controller):
        self._controller = controller
        for virtualMachine in self._virtualMachines:
            virtualMachine.setController(controller)

    def receiveRequest(self, request: Request):
        print('Received request from controller')
        vm = self._chooseVirtualMachine(request)
        self._respondToController(request, vm)
    
    def run(self):
        while True:
            time.sleep(1)
            self._pingVirtualMachines()
            if self._killed == True:
                break
    
    def _chooseVirtualMachine(self, item: Request) -> VirtualMachine:
        print(f'Querying VMs...')
        # TODO: implement the algorithm for choosing VMs
        vm = self._virtualMachines[random.randint(0, len(self._virtualMachines) - 1)]
        print(f'Found VM: {vm}.')
        return vm

    def _respondToController(self, request: Request, virtualMachine: VirtualMachine):
        self._controller.receiveLoadBalancerDecision(request, virtualMachine)
    
    def _pingVirtualMachines(self):
        # TODO: find a thread safe solution
        for virtualMachine in self._virtualMachines:
            self._virtualMachinesDictionary[virtualMachine] = virtualMachine.runningPercentage

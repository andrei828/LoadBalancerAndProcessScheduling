from __future__ import annotations
from virtualMachine import VirtualMachine
from controller import Controller
from threading import Thread
from typing import List
import threading, queue

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller import Controller

class LoadBalancer(Thread):
    
    def __init__(self, virtualMachines: List[VirtualMachine]):
        Thread.__init__(self)
        self._killed = False
        self._queue = queue.Queue()
        self._virtualMachines = virtualMachines

    def __del__(self):
        # wait for tasks to finish
        self._queue.join()
    
    def initialize(self) -> LoadBalancer:
        self.start()
        return self
    
    def setController(self, controller: Controller):
        self._controller = controller

    def _chooseVirtualMachine(self, item: Request) -> VirtualMachine:
        print(f'Querying VMs...')
        print(f'Found VM: {self._virtualMachines[0]}.')
        return self._virtualMachines[0]

    def _respondToController(self, virtualMachine: VirtualMachine):
        self._controller.setVirtualMachineForRequest(virtualMachine)

    def sendRequest(self, request: Request):
        print('Received request from controller')
        self._queue.put(request)

    def run(self):
        while True:
            try:
                item = self._queue.get(True, 2)
                vm = self._chooseVirtualMachine(item)
                self._respondToController(vm)
                self._queue.task_done()
            except queue.Empty:
                if self._killed == True:
                    break
    
    def stop(self):
        self._killed = True

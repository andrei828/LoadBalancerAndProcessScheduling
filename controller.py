from __future__ import annotations
from threading import Thread
from request import Request
import threading, queue

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from loadBalancer import LoadBalancer
    from virtualMachine import VirtualMachine

class Controller(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        self._killed = False
        self._queue = queue.Queue()

    def __del__(self):
        # wait for tasks to finish
        self._queue.join()
    
    def initialize(self) -> Controller:
        self.start()
        return self
    
    def stop(self):
        self._killed = True

    def setLoadBalancer(self, loadBalancer: LoadBalancer):
        self._loadBalancer = loadBalancer

    def sendRequest(self, request: Request):
        print("Received request from client")
        self._queue.put(request)
    
    def setVirtualMachineForRequest(self, virtualMachine: VirtualMachine):
        print(f'Chossing VM: {virtualMachine}.')
        self._queue.task_done()

    def run(self):
        while True:
            try:
                item = self._queue.get(True, 2)
                self._queryLoadBalancer(item)
            except queue.Empty:
                if self._killed == True:
                    break
    
    def _queryLoadBalancer(self, item: Request):
        self._loadBalancer.sendRequest(item)

    

    
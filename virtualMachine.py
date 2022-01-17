from __future__ import annotations
from threading import Thread
from request import Request
import threading, queue

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from loadBalancer import LoadBalancer
    from controller import Controller

class VirtualMachine(Thread):
    def __init__(self):
        Thread.__init__(self)
        self._killed = False
        self.runningPercentage = 0
        self._queue = queue.Queue()

    def __del__(self):
        # wait for tasks to finish
        self._queue.join()
    
    def initialize(self) -> Controller:
        self.start()
        return self
    
    def stop(self):
        self._killed = True

    def setController(self, controller: Controller):
        self._controller = controller

    def setLoadBalancer(self, loadBalancer: LoadBalancer):
        self._loadBalancer = loadBalancer

    def receiveRequest(self, request: Request):
        self._queue.put(request)

    def run(self):
        while True:
            try:
                request = self._queue.get(True, 2)
                self._handleRequest(request)
            except queue.Empty:
                if self._killed == True:
                    break
    
    def _handleRequest(self, request: Request):
        # TODO: implement the algorithm
        print("Working on the Task")
        self._queue.task_done()
        self._notifyController(request)
    
    def _notifyController(self, request: Request):
        self._controller.receiveResponseFromVm(request, self)

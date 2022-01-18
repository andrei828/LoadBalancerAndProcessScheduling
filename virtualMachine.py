from __future__ import annotations
from datetime import datetime
from threading import Thread
from request import Request
import threading, queue
import uuid
import json

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from loadBalancer import LoadBalancer
    from controller import Controller

class VirtualMachine(Thread):
    def __init__(self, name = None):
        Thread.__init__(self)
        self._killed = False
        self.runningPercentage = 0
        self._queue = queue.Queue()
        self._logger = open(f'logs/VM-{self.name}.log', 'a')
        #self.name = str(uuid.uuid4()) if name == None else name

    def __del__(self):
        # wait for tasks to finish
        self._queue.join()
    
    def initialize(self) -> Controller:
        self.start()
        self._printLog(f'Starting virtual machine {self.name}...')
        return self
    
    def stop(self):
        self._killed = True
        self._printLog(f'Stopping virtual machine {self.name}...')

    def setController(self, controller: Controller):
        self._controller = controller

    def setLoadBalancer(self, loadBalancer: LoadBalancer):
        self._loadBalancer = loadBalancer

    def receiveRequest(self, request: Request):
        self._printLog(f'Received request [{request.name}] with {len(request.tasks)} Tasks.')
        self._printLog(f'Enquing the request...')
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
        print("Working on the Task")
        self._printLog(f'Processing request [{request.name}]...')

        # TODO: implement the algorithm
        
        self._queue.task_done()
        self._printLog(f'Finished request [{request.name}].')
        self._notifyController(request)
    
    def _notifyController(self, request: Request):
        self._printLog(f'Notifying the controller request [{request.name}] has finished.')
        self._controller.receiveResponseFromVm(request, self)
    
    def _printLog(self, content: str):
        self._logger.write(f'[{datetime.now()}] {content}\n')

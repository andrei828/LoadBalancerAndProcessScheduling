from __future__ import annotations
from datetime import datetime
from threading import Thread
from logger import Logger
from logging_level import LoggingLevel
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
        self._logger = Logger('Controller.log')

    def __del__(self):
        # wait for tasks to finish
        self._queue.join()
    
    def initialize(self) -> Controller:
        self._logger.log(f'Starting Controller...')
        self.start()
        return self
    
    def stop(self):
        self._killed = True
        self._logger.log(f'Stopping Controller and all associated VMs...')

    def setLoadBalancer(self, loadBalancer: LoadBalancer):
        self._loadBalancer = loadBalancer

    def receiveRequest(self, request: Request):
        self._logger.log(f'Received request [{request.name}] with {len(request.tasks)} Tasks.')
        self._queue.put(request)

    def receiveResponseFromVm(self, request: Request, virtualMachine: VirtualMachine):
        print('Done request')
    
    def receiveLoadBalancerDecision(self, request: Request, virtualMachine: VirtualMachine):
        print(f'Chossing VM: {virtualMachine}.')
        self._logger.log(f'Load Balancer has chosen Virtual Machine [{virtualMachine.name}] for request [{request.name}]')
        self._queue.task_done()
        self._sendToVm(request, virtualMachine)

    def run(self):
        while True:
            try:
                request = self._queue.get(True, 2)
                self._queryLoadBalancer(request)
            except queue.Empty:
                if self._killed == True:
                    break
        self._logger.log(f'Controller stopped.')
    
    def _queryLoadBalancer(self, request: Request):
        self._logger.log(f'Querying Load Balancer for request [{request.name}]', LoggingLevel.VERBOSE)
        self._loadBalancer.receiveRequest(request)
    
    def _sendToVm(self, request: Request, virtualMachine: VirtualMachine):
        self._logger.log(f'Sending request [{request.name}] to virtualMachine [{virtualMachine.name}]')
        virtualMachine.receiveRequest(request)

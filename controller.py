from __future__ import annotations
from datetime import datetime
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
        self._logger = open(f'logs/Controller.log', 'a')

    def __del__(self):
        # wait for tasks to finish
        self._queue.join()
    
    def initialize(self) -> Controller:
        self._printLog(f'Starting Controller...')
        self.start()
        return self
    
    def stop(self):
        self._killed = True
        self._printLog(f'Stopping Controller and all associated VMs...')

    def setLoadBalancer(self, loadBalancer: LoadBalancer):
        self._loadBalancer = loadBalancer

    def receiveRequest(self, request: Request):
        self._printLog(f'Received request [{request.name}] with {len(request.tasks)} Tasks.')
        self._queue.put(request)

    def receiveResponseFromVm(self, request: Request, virtualMachine: VirtualMachine):
        print('Done request')
    
    def receiveLoadBalancerDecision(self, request: Request, virtualMachine: VirtualMachine):
        print(f'Chossing VM: {virtualMachine}.')
        self._printLog(f'Load Balancer has chosen Virtual Machine [{virtualMachine.name}] for request [{request.name}]')
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
        self._printLog(f'Controller stopped.')
    
    def _queryLoadBalancer(self, request: Request):
        self._printLog(f'Querying Load Balancer for request [{request.name}]')
        self._loadBalancer.receiveRequest(request)
    
    def _sendToVm(self, request: Request, virtualMachine: VirtualMachine):
        self._printLog(f'Sending request [{request.name}] to virtualMachine [{virtualMachine.name}]')
        virtualMachine.receiveRequest(request)
    
    def _printLog(self, content: str):
        self._logger.write(f'[{datetime.now()}] {content}\n')

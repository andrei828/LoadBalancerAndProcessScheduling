from __future__ import annotations
from threading import Thread
from datetime import datetime
import threading, queue
import json
import copy
import time
from json import JSONEncoder

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from request import Request
    from loadBalancer import LoadBalancer
    from virtualMachine import VirtualMachine

class CustomJsonEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class VirtualMachineDiagnosticService(Thread):

    def __init__(self, virtualMachines: [VirtualMachine] = None):
        Thread.__init__(self)
        self._killed = False
        self._virtualMachines = virtualMachines
        self._logger = open(f'logs/VirtualMachineDiagnosticService.log', 'a')
    
    def initialize(self) -> VirtualMachineDiagnosticService:
        self._printLog(f'Starting virtual machine diagnostic service...')
        self.start()
        return self
    
    def stop(self):
        self._killed = True
        self._printLog(f'Stopping virtual machine diagnostic service...')
    
    def run(self):
        while True:
            print("Running Diagnostic...")
            self._printLog("Running Diagnostic...")
            self.queryVirtualMachinesState()
            time.sleep(1)
            if self._killed == True:
                break
        self._printLog(f'Virtual Machine Diagnostic Service stopped.')

    def queryVirtualMachinesState(self):
        virtualMachinesState = {}
        for virtualMachine in self._virtualMachines:
            self._printLog(f'Locking Virtual Machine [{virtualMachine.name}]...')
            virtualMachine.lockThread()

            currentLoad = copy.deepcopy(virtualMachine.getCurrentLoad())
            runningPercentage = virtualMachine.runningPercentage

            self._printLog(f'Releasing Virtual Machine [{virtualMachine.name}]...')
            virtualMachine.unlockThread()

            virtualMachinesState[virtualMachine.name] = { 'percentage': runningPercentage, 'queue': currentLoad }
        
        self._printLog(json.dumps(virtualMachinesState, cls=CustomJsonEncoder))
        return virtualMachinesState

    def _printLog(self, content: str):
        self._logger.write(f'[{datetime.now()}] {content}\n')

    
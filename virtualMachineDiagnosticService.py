from __future__ import annotations
from re import VERBOSE
from json import JSONEncoder
from threading import Thread
from datetime import datetime
from functools import reduce
import threading, queue
import json
import copy
import time

from typing import TYPE_CHECKING, List
from logger import Logger

from logging_level import LoggingLevel
if TYPE_CHECKING:
    from request import Request
    from loadBalancer import LoadBalancer
    from virtualMachine import VirtualMachine

class CustomJsonEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class VirtualMachineDiagnosticService(Thread):

    def __init__(self, virtualMachines: List[VirtualMachine] = None):
        Thread.__init__(self)
        self._killed = False
        self._virtualMachines = virtualMachines
        self._logger = Logger(f'VirtualMachineDiagnosticService.log')
    
    def initialize(self) -> VirtualMachineDiagnosticService:
        self._logger.log(f'Starting virtual machine diagnostic service...')
        self.start()
        return self
    
    def stop(self):
        self._killed = True
        self._logger.log(f'Stopping virtual machine diagnostic service...')
    
    def run(self):
        while True:
            self._logger.log("Running Diagnostic...", LoggingLevel.VERBOSE)
            self.queryVirtualMachinesState()
            time.sleep(1)
            if self._killed == True:
                break
        self._logger.log(f'Virtual Machine Diagnostic Service stopped.')

    def queryVirtualMachinesState(self):
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
            
            runningPercentage = min(1, round(0.05 + totalDurationForVm / 1000, 3))
            
            self._logger.log(f'Releasing Virtual Machine [{virtualMachine.name}]...', LoggingLevel.VERBOSE)
            virtualMachine.unlockThread()

            virtualMachinesState[virtualMachine.name] = { 'percentage': runningPercentage, 'queue': currentLoad }
        
        # self._logger.log(str(json.dumps(virtualMachinesState, cls=CustomJsonEncoder)), LoggingLevel.VERBOSE)
        return json.loads(json.dumps(virtualMachinesState, cls=CustomJsonEncoder))


    
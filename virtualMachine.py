from __future__ import annotations
from asyncio import tasks
from copy import copy
from datetime import datetime
from threading import Thread, Lock
from logger import Logger
from logging_level import LoggingLevel
from request import Request
import queue
import uuid
import json
import time

from typing import TYPE_CHECKING, List

from task import Task
if TYPE_CHECKING:
    from loadBalancer import LoadBalancer
    from controller import Controller

class VirtualMachine(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.lock = Lock()
        self._killed = False
        self.runningRequest = None
        self._queue = queue.Queue()
        self._logger = Logger(f'VM-{self.name}.log')

    def __del__(self):
        # wait for tasks to finish
        self._queue.join()
    
    def initialize(self) -> VirtualMachine:
        self._logger.log(f'Starting virtual machine [{self.name}]...')
        self.start()
        return self
    
    def stop(self):
        self._killed = True
        self._logger.log(f'Stopping virtual machine [{self.name}]...')

    def setController(self, controller: Controller):
        self._controller = controller

    def setLoadBalancer(self, loadBalancer: LoadBalancer):
        self._loadBalancer = loadBalancer

    def receiveRequest(self, request: Request):
        self._logger.log(f'Received request [{request.name}] with {len(request.tasks)} Tasks.')
        self._logger.log(f'Enquing the request...')
        self._queue.put(request)
    
    def getCurrentLoad(self) -> List[Request]:
        self._logger.log(f'Getting queried for current state', LoggingLevel.VERBOSE)
        return list(self._queue.queue)

    def run(self):
        while True:
            try:
                request = self._queue.get(True, 2)
                self._handleRequest(request)
            except queue.Empty:
                if self._killed == True:
                    break
        self._logger.log(f'Virtual Machine {self.name} stopped.')
    
    def _handleRequest(self, request: Request):
        print("Working on the Task")
        self._logger.log(f'Processing request [{request.name}]...')

        self.runningRequest = request
        self._processTasks(request)
        self._queue.task_done()
        self.runningRequest = None
        
        self._logger.log(f'Finished request [{request.name}].')
        self._notifyController(request)
    
    def _notifyController(self, request: Request):
        self._logger.log(f'Notifying the controller request [{request.name}] has finished.')
        self._controller.receiveResponseFromVm(request, self)
    
    def lockThread(self):
        self.lock.acquire()
    
    def unlockThread(self):
        self.lock.release()

    def _sleepForTask(task: Task):
        while task.duration > 0:
            sleepTime = min(task.duration, 0.5)
            time.sleep(sleepTime)
            task.duration -= sleepTime

    def _processTasks(self, request: Request):
        request.tasks.sort(key=lambda x: x.duration)
        while True:
            if len(request.tasks) <= 0:
                return
            tq = self._calculateTQ(request.tasks)
            task = request.tasks[0]
            if task.duration - tq <= 0:
                self._logger.log(f'processing Task {task.name} in {task.duration}')
                VirtualMachine._sleepForTask(task)
            else:
                task.duration = task.duration - tq
                request.tasks.append(copy.deepcopy(task))
                self._logger.log(f'processing Task {task.name} in {tq}')
                VirtualMachine._sleepForTask(task)
            request.tasks.pop(0)

    def _calculateTQ(self, tasks: List[Task]):
        size = len(tasks)
        if size%2:
            median = tasks[size // 2].duration
        else:
            median = (tasks[size // 2 - 1].duration + tasks[size // 2].duration) // 2
        mean = sum(t.duration for t in tasks) / size

        return (mean + median) // 2

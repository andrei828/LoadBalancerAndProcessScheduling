from task import Task
from typing import List

class Request:
    def __init__(self, tasks: List[Task]):
        self.tasks = tasks
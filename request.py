import uuid
from task import Task
from typing import List

class Request:
    def __init__(self, tasks: List[Task], name = None):
        self.tasks = tasks
        self.name = str(uuid.uuid4()) if name == None else name


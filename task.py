import uuid

class Task:
    def __init__(self, duration, name = None):
        self.duration = duration
        self.name = str(uuid.uuid4()) if name == None else name
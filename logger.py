from datetime import datetime
from multiprocessing import Lock
from logging_level import LoggingLevel
from global_vars import LOGGING_LEVEL

class Logger():
  file_name: str = None

  def __init__(self, file_name: str):
    self.lock = Lock()
    self.last_read_byte = 0
    self.file_name = file_name
    self._logger = open(f'logs/{file_name}', 'w+')

  def __del__(self):
    self._logger.close()
  
  def log(self, content: str, level: LoggingLevel = LoggingLevel.INFO):
    if level <= LOGGING_LEVEL:
      self.lock.acquire()
      self._logger.write(f'[{level.name}] [{datetime.now()}] {content}\n')
      self._logger.flush()
      self.lock.release()

  def read_logs(self):
    self.lock.acquire()
    self._logger.seek(self.last_read_byte)
    str = self._logger.read()
    self.last_read_byte = self._logger.tell()
    self.lock.release()
    return str

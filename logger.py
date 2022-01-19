from datetime import datetime
from logging_level import LoggingLevel
from global_vars import LOGGING_LEVEL

class Logger:
  def __init__(self, file_name: str):
    self._logger = open(f'logs/{file_name}', 'w')

  def __del__(self):
    self._logger.close()
  
  def log(self, content: str, level: LoggingLevel = LoggingLevel.INFO):
    if level <= LOGGING_LEVEL:
      self._logger.write(f'[{level.name}] [{datetime.now()}] {content}\n')
      self._logger.flush()
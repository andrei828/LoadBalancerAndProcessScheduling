
from enum import Enum
from functools import total_ordering


@total_ordering
class LoggingLevel(Enum):
  ERROR = 1
  INFO = 2
  VERBOSE = 3

  def __lt__(self, other):
    if self.__class__ is other.__class__:
      return self.value < other.value
    return NotImplemented

  def __eq__(self, other):
    if self.__class__ is other.__class__:
      return self.value == other.value
    return NotImplemented
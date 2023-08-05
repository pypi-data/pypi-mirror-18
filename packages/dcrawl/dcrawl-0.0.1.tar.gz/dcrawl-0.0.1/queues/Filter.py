from .Abstract import AbstractQueue

"""
  A queue which only sends objects which
  pass an acceptance test.

  Eg. use for restricting a crawl to a
  set of domains.
"""

class FilterQueue(AbstractQueue):

  def __init__(self, queue, accept):
    self.accept = accept
    self.queue = queue

    self.get = queue.get

  def send(self, things):
    self.queue.send(filter(self.accept, things))

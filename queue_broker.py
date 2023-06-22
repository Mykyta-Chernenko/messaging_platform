import abc
import queue


# TODO very simplistic interface
class Queue:
    @abc.abstractmethod
    def get(self, timeout=None):
        """returns one object"""
        raise NotImplementedError

    @abc.abstractmethod
    def put(self, obj):
        """puts one object in the queue"""
        raise NotImplementedError


class QueueConnector(abc.ABC):
    @abc.abstractmethod
    def connect(self) -> Queue:
        """returns queue connection"""
        raise NotImplementedError


# TODO this is a simplistic queue that can be replaced with a more sophisticated solution is e.g. rabbitmq
class LocalQueueConnector(QueueConnector):
    def __init__(self):
        self.queue = queue.Queue()

    def connect(self) -> Queue:
        return self.queue

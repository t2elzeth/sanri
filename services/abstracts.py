from abc import ABC, abstractmethod


class IService(ABC):
    @abstractmethod
    def __init__(self, dto):
        pass

    @abstractmethod
    def execute(self):
        pass

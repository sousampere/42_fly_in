
from abc import ABC, abstractmethod

from src.MapState import State


class AbstractStateProcessor(ABC):
    @abstractmethod
    def yield_process(state: State):
        """ Process each turn by yielding
        the current State progression """
        pass

# class StateProcessor(AbstractStateProcessor):
#     for 
from abc import ABC, abstractmethod
from typing import Dict


class AbstractOutput(ABC):
    @abstractmethod
    def output(self, rankings: Dict[int, float]) -> None:
        raise NotImplementedError()
from typing import Any
from abc import ABC, abstractmethod

class BaseBroker(ABC):

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def place_order(self, symbol: str, side: str, quantity: int):
        pass

    @abstractmethod
    def get_holdings(self) -> Any:
        pass
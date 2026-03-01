from abc import ABC, abstractmethod
import pandas as pd


class CyberAttack(ABC):
    """
    Abstract base class for cyber attacks.
    """

    @abstractmethod
    def apply(self, net, current_time: pd.Timestamp) -> float:
        """
        Applies attack logic and returns fleet multiplier.
        """
        pass
from abc import ABC, abstractmethod
from typing import Dict, Optional


class AtmHandler(ABC):
    @abstractmethod
    def load_data(self) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_users(self) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_passwords(self) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_accounts(self) -> Optional[Dict]:
        pass

    @abstractmethod
    def save_data(self, users: Optional[Dict], passwords: Optional[Dict], accounts: Optional[Dict]) -> bool:
        pass

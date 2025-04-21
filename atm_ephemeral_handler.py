import logging
from typing import Dict, Optional

from atm_handler import AtmHandler


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# ATM File Handler to manage data storage and retrieval
# This class handles the loading and saving of ATM data to a JSON file.
class AtmEphemeralHandler(AtmHandler):
    def __init__(self) -> None:
        super().__init__()
        self.data: Optional[Dict] = None
        self.users: Optional[Dict] = None
        self.passwords: Optional[Dict] = None
        self.accounts: Optional[Dict] = None

    def load_data(self) -> Optional[Dict]:
        self.data = {
  "users": {
    "1": {
      "name": "John Doe",
      "email": ""
    },
    "2": {
      "name": "Jane Smith",
      "email": ""
    }
  },
  "passwords": {
    "1": {
      "password": "111"
    },
    "2": {
      "password": "qwerty"
    }
  },
  "accounts": {
    "1": {
      "owner_id": "1",
      "balance": 1000,
      "account_id": "1"
    },
    "2": {
      "owner_id": "1",
      "balance": 2000,
      "account_id": "2"
    },
    "3": {
      "owner_id": "2",
      "balance": 1500,
      "account_id": "3"
    },
    "4": {
      "owner_id": "2",
      "balance": 2500,
      "account_id": "4"
    }
  }
}

        return self.data

    def get_users(self) -> Optional[Dict]:
        if self.data is None:
            self.load_data()
        return self.data.get('users')

    def get_passwords(self) -> Optional[Dict]:
        if self.data is None:
            self.load_data()
        return self.data.get('passwords')

    def get_accounts(self) -> Optional[Dict]:
        if self.data is None:
            self.load_data()
        return self.data.get('accounts')

    def save_data(self, users: Optional[Dict], passwords: Optional[Dict], accounts: Optional[Dict]) -> bool:
        # do nothing
        return True

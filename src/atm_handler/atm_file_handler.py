import json
import logging
from typing import Dict, Optional

from atm_handler.atm_handler import AtmHandler
from dao import Account, Password, User


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# ATM File Handler to manage data storage and retrieval
# This class handles the loading and saving of ATM data to a JSON file.
class AtmFileHandler(AtmHandler):
    def __init__(self, data_file: str = 'data.json') -> None:
        self.data_file: str = data_file
        self.data: Optional[Dict] = None
        self.users: Optional[Dict[str, User]] = None
        super().__init__()
        self.passwords: Optional[Dict[str, Password]] = None
        self.accounts: Optional[Dict[str, Account]] = None

    def load_data(self) -> Optional[Dict]:
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            logging.error(f"File '{self.data_file}' not found.")
            self.data = {}
        except json.JSONDecodeError:
            logging.error(f"Failed to decode JSON from file '{self.data_file}'.")
            self.data = {}
        except Exception as e:
            logging.error(f"An unexpected error occurred while loading data: {e}")
            self.data = {}
        return self.data

    def get_users(self) -> Dict[str, User]:
        # Deserialize
        if self.data is None:
            self.load_data()
        users = {uid: User.from_dict(info) for uid, info in self.data["users"].items()}
        return users

    def get_passwords(self) -> Dict[str, Password]:
        if self.data is None:
            self.load_data()
        passwords = {uid: Password.from_dict(info) for uid, info in self.data["passwords"].items()}
        return passwords

    def get_accounts(self) -> Dict[str, Account]:
        if self.data is None:
            self.load_data()
        accounts = {uid: Account.from_dict(info) for uid, info in self.data["accounts"].items()}
        return accounts

    def save_data(self, users: Dict[str, User], passwords: Dict[str, Password], accounts: Dict[str, Account]) -> bool:
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json_data = {
                           "users": {uid: user.to_dict() for uid, user in users.items()},
                            "passwords": {uid: pw.to_dict() for uid, pw in passwords.items()},
                            "accounts": {aid: acc.to_dict() for aid, acc in accounts.items()}
                }
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            logging.error(f"Failed to write to file '{self.data_file}': {e}")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred while saving data: {e}")
            return False

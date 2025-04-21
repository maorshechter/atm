import json
import logging
from typing import Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class AtmFileHandler:
    def __init__(self, data_file: str = 'data.json') -> None:
        self.data_file: str = data_file
        self.data: Optional[Dict] = None
        self.users: Optional[Dict] = None
        self.passwords: Optional[Dict] = None
        self.accounts: Optional[Dict] = None

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
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump({'users': users, 'passwords': passwords, 'accounts': accounts}, f, indent=2,
                           ensure_ascii=False)
            return True
        except IOError as e:
            logging.error(f"Failed to write to file '{self.data_file}': {e}")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred while saving data: {e}")
            return False

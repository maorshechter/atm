import logging
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# ATM class to manage customer accounts and transactions
class ATM:
    def __init__(self, users: Optional[Dict],
                  passwords: Optional[Dict],
                  accounts: Optional[Dict]) -> None:

        self.users = users
        self.passwords = passwords
        self.accounts = accounts
        self.specific_user = None

        # build an index of accounts by owner_id for faster access
        self.accounts_by_owner: Dict[str, List[dict]] = self.build_owner_account_index()

    def build_owner_account_index(self) -> None:
        for account in self.accounts:
            owner_id = account['owner_id']
            if owner_id not in self.accounts_by_owner:
                self.accounts_by_owner[owner_id] = []
            self.accounts_by_owner[owner_id].append(account)

    def authenticate(self, username: str, password: str) -> bool:
        if self.passwords['username'] == username and self.passwords['password'] == password:
            self.specific_user = username
            return True
        logging.error("Authentication failed: Invalid username or password.")
        return False

    def authenticated_user_required(func):
        def wrapper(self, *args, **kwargs):
            if not self.specific_user:
                raise Exception("Operation not allowed: User must be authenticated.")
            return func(self, *args, **kwargs)
        return wrapper

    @authenticated_user_required
    def get_balance(self) -> Dict[str, float]:
        return {account: account['balance'] for account in self.accounts_by_owner[self.specific_user]}

    @authenticated_user_required
    def withdraw(self, account_id: str, amount: float) -> bool:
        if not self._can_withdraw(account_id, amount):
            self._log_withdraw_error(account_id, amount)
            return False
        self.accounts[account_id]['balance'] -= amount
        return True

    def _can_withdraw(self, account_id: str, amount: float) -> bool:
        return (
            amount > 0 and
            account_id in self.accounts and
            self.accounts[account_id]['owner_id'] == self.specific_user and
            self.accounts[account_id]['balance'] >= amount
        )

    def _log_withdraw_error(self, account_id: str, amount: float) -> None:
        if amount <= 0:
            logging.error("Withdrawal failed: Amount must be positive.")
        elif account_id not in self.accounts:
            logging.error("Withdrawal failed: Account not found.")
        elif self.accounts[account_id]['owner_id'] != self.specific_user:
            logging.error("Withdrawal failed: Unauthorized access.")
        elif self.accounts[account_id]['balance'] < amount:
            logging.error("Withdrawal failed: Insufficient funds.")

    @authenticated_user_required
    def deposit(self, account_id: str, amount: float) -> bool:
        if not self._can_deposit(account_id, amount):
            self._log_deposit_error(account_id, amount)
            return False
        self.accounts[account_id]['balance'] += amount
        return True

    def _can_deposit(self, account_id: str, amount: float) -> bool:
        return (
            amount > 0 and
            account_id in self.accounts and
            self.accounts[account_id]['owner_id'] == self.specific_user
        )

    def _log_deposit_error(self, account_id: str, amount: float) -> None:
        if amount <= 0:
            logging.error("Deposit failed: Amount must be positive.")
        elif account_id not in self.accounts:
            logging.error("Deposit failed: Account not found.")
        elif self.accounts[account_id]['owner_id'] != self.specific_user:
            logging.error("Deposit failed: Unauthorized access.")

    @authenticated_user_required
    def transfer(self, from_account: str, to_account: str, amount: float) -> bool:
        if not self._can_transfer(from_account, to_account, amount):
            self._log_transfer_error(from_account, to_account, amount)
            return False
        self.accounts[from_account]['balance'] -= amount
        self.accounts[to_account]['balance'] += amount
        return True

    def _can_transfer(self, from_account: str, to_account: str, amount: float) -> bool:
        return (
            amount > 0 and
            from_account in self.accounts and
            to_account in self.accounts and
            self.accounts[from_account]['owner_id'] == self.specific_user
        )

    def _log_transfer_error(self, from_account: str, to_account: str, amount: float) -> None:
        if amount <= 0:
            logging.error("Transfer failed: Amount must be positive.")
        elif from_account not in self.accounts:
            logging.error("Transfer failed: From account not found.")
        elif to_account not in self.accounts:
            logging.error("Transfer failed: To account not found.")
        elif self.accounts[from_account]['owner_id'] != self.specific_user:
            logging.error("Transfer failed: Unauthorized access.")
        elif self.accounts[from_account]['balance'] < amount:
            logging.error("Transfer failed: Insufficient funds.")

    @authenticated_user_required
    def change_password(self, new_password: str) -> bool:
        if not self._is_valid_password(new_password):
            logging.error("Password change failed: Invalid password.")
            return False
        self.passwords[self.specific_user] = new_password
        return True

    def _is_valid_password(self, password: str) -> bool:
        return bool(password)

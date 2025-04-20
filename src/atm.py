import logging
from typing import Dict, List, Optional
from exceptions import UnauthorizedAccessError, InvalidAmountError, AccountNotFoundError, ATMError
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
        self.accounts_by_owner: Dict[str, List[dict]] = {}
        self.build_owner_account_index()
        
    def build_owner_account_index(self) -> None:
        for account in self.accounts:
            owner_id = self.accounts[account]['owner_id']
            if owner_id not in self.accounts_by_owner:
                self.accounts_by_owner[owner_id] = []
            data = self.accounts[account]
            self.accounts_by_owner[owner_id].append(data)

    def authenticate(self, user_id: str, password: str) -> str:
        if user_id in self.passwords and self.passwords[user_id]['password'] == password:
            self.specific_user = user_id
            logging.info(f"User '{user_id}' authenticated successfully.")
            return self.users[user_id]['name']
        raise UnauthorizedAccessError("Authentication failed: Invalid username or password.")
    
    def authenticated_user_required(func):
        def wrapper(self, *args, **kwargs):
            if not self.specific_user:
                raise UnauthorizedAccessError("Operation not allowed: User must be authenticated.")
            return func(self, *args, **kwargs)
        return wrapper

    @authenticated_user_required
    def get_balance(self) -> Dict[str, float]:
        return {account['account_id']: account['balance'] for account in self.accounts_by_owner[self.specific_user]}

    @authenticated_user_required
    def withdraw(self, account_id: str, amount: float) -> None:
        if not self._can_withdraw(account_id, amount):
            self._raise_withdraw_error(account_id, amount)
        self.accounts[account_id]['balance'] -= amount

    def _can_withdraw(self, account_id: str, amount: float) -> bool:
        # if more condition in future maybe redisnign this method
        return (
            amount > 0 and
            account_id in self.accounts and
            self.accounts[account_id]['owner_id'] == self.specific_user
        )

    def _raise_withdraw_error(self, account_id: str, amount: float) -> None:
        if amount <= 0:
            raise InvalidAmountError("Withdrawal failed: Amount must be positive.")
        elif account_id not in self.accounts:
            raise AccountNotFoundError("Withdrawal failed: Account not found.")
        elif self.accounts[account_id]['owner_id'] != self.specific_user:
            raise UnauthorizedAccessError("Withdrawal failed: Unauthorized access.")
        
    @authenticated_user_required
    def deposit(self, account_id: str, amount: float) -> None:
        if not self._can_deposit(account_id, amount):
            self._raise_deposit_error(account_id, amount)
        self.accounts[account_id]['balance'] += amount

    def _can_deposit(self, account_id: str, amount: float) -> bool:
        return (
            amount > 0 and
            account_id in self.accounts and
            self.accounts[account_id]['owner_id'] == self.specific_user
        )

    def _raise_deposit_error(self, account_id: str, amount: float) -> None:
        if amount <= 0:
            raise InvalidAmountError("Deposit failed: Amount must be positive.")
        elif account_id not in self.accounts:
            raise AccountNotFoundError("Deposit failed: Account not found.")
        elif self.accounts[account_id]['owner_id'] != self.specific_user:
            raise UnauthorizedAccessError("Deposit failed: Unauthorized access.")

    @authenticated_user_required
    def transfer(self, from_account: str, to_account: str, amount: float) -> None:
        if not self._can_transfer(from_account, to_account, amount):
            self._raise_transfer_error(from_account, to_account, amount)
        from_account_balance = self.accounts[from_account]['balance']
        to_account_balance = self.accounts[to_account]['balance']
        try:
            self.accounts[from_account]['balance'] -= amount
            self.accounts[to_account]['balance'] += amount
        except Exception as e:
            logging.error(f"Transfer failed: {e}, rollback initiated.")
            # Rollback the transaction in case of an error
            self.accounts[from_account]['balance'] = from_account_balance
            self.accounts[to_account]['balance'] = to_account_balance
            raise ATMError("Transfer failed due to an unexpected error.")

    def _can_transfer(self, from_account: str, to_account: str, amount: float) -> bool:
        return (
            amount > 0 and
            from_account in self.accounts and
            to_account in self.accounts and
            self.accounts[from_account]['owner_id'] == self.specific_user
        )

    def _raise_transfer_error(self, from_account: str, to_account: str, amount: float) -> None:
        if amount <= 0:
            raise InvalidAmountError("Transfer failed: Amount must be positive.")
        elif from_account not in self.accounts:
            raise AccountNotFoundError("Transfer failed: From account not found.")
        elif to_account not in self.accounts:
            raise AccountNotFoundError("Transfer failed: To account not found.")
        elif self.accounts[from_account]['owner_id'] != self.specific_user:
            raise UnauthorizedAccessError("Transfer failed: Unauthorized access.")
        
    @authenticated_user_required
    def change_password(self, new_password: str) -> None:
        if not self._is_valid_password(new_password):
            raise Exception("Password change failed: Invalid password.")
        self.passwords[self.specific_user]["password"] = new_password
        logging.info("Password changed successfully.")

    def _is_valid_password(self, password: str) -> bool:
        return bool(password)
    
    def get_users(self) -> Dict:
        return self.users

    def get_passwords(self) -> Dict:
        return self.passwords

    def get_accounts(self) -> Dict:
        return self.accounts
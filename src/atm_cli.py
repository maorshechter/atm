from atm import ATM, ATMError, UnauthorizedAccessError, AccountNotFoundError, InvalidAmountError
from atm_handler.atm_handler import AtmHandler

# io_interface.py
class IOInterface:
    def input(self, prompt: str) -> str:
        return input(prompt)

    def print(self, message: str) -> None:
        print(message)


class ATMCLI:
    def __init__(self, atm_handler: AtmHandler = None) -> None:
        # load data from file
        self.atm_handler = atm_handler

        self.io_interface = IOInterface()
        # init atm instance with data from file
        self.atm = ATM(self.atm_handler.get_users(), 
                    self.atm_handler.get_passwords(),
                    self.atm_handler.get_accounts())
        
        # Scalable menu actions
        self.menu_actions = {
            "1": ("Check balance", self.handle_balance),
            "2": ("Withdraw cash", self.handle_withdraw),
            "3": ("Deposit cash", self.handle_deposit),
            "4": ("Change password", self.handle_change_password),
            "5": ("Transfer to another account", self.handle_transfer),
            "6": ("Logout", None),
        }

    def run(self):
        while True:
            self.io_interface.print("\nWelcome to the ATM")
            user_id = self.io_interface.input("Enter user_id (or -1 to exit): ")
            if user_id == "-1":
                break
            password = self.io_interface.input("Enter password: ")
            try:
                username = self.atm.authenticate(user_id, password)
                self.io_interface.print(f"Hello, {username}!")
                self.account_menu()
            except UnauthorizedAccessError as e:
                self.io_interface.print(f"Authentication failed: {e}")
            except Exception as e:
                self.io_interface.print(f"An unexpected error occurred: {e}")

        try:
            self.atm_handler.save_data(
                self.atm.get_users(),
                self.atm.get_passwords(),
                self.atm.get_accounts(),
            )
            self.io_interface.print("Customer data saved. Goodbye!")
        except Exception as e:
            self.io_interface.print(f"Failed to save customer data: {e}")

    def account_menu(self):
        while True:
            self.io_interface.print("\n--- ATM Menu ---")
            for key, (desc, _) in self.menu_actions.items():
                self.io_interface.print(f"{key}. {desc}")

            choice = self.io_interface.input("Choose an option: ")
            action = self.menu_actions.get(choice)

            if action:
                _, func = action
                if func:
                    func()
                else:
                    self.io.print("Logging out...")
                    break
            else:
                self.io_interface.print("Invalid option.")

    def handle_change_password(self):
        new_password = self.io_interface.input("Enter new password: ")
        try:
            self.atm.change_password(new_password)
            self.io_interface.print("Password changed successfully.")
        except Exception as e:
            self.io_interface.print(f"Failed to change password: {e}")

    def handle_balance(self):
        try:
            balance = self.atm.get_balance()
            self.io_interface.print(f"Your balance is: {balance}")
        except Exception as e:
            self.io_interface.print(f"Failed to retrieve balance: {e}")

    def handle_withdraw(self):
        acc_num = self.io_interface.input("Account number: ")
        try:
            amount = float(self.io_interface.input("Amount to withdraw: "))
            self.atm.withdraw(account_id=acc_num, amount=amount)
            self.io_interface.print(f"Withdrew {amount} from account {acc_num}.")
        except ATMError as e:
            self.io_interface.print(f"Withdrawal failed: {e}")

    def handle_deposit(self):
        acc_num = self.io_interface.input("Account number: ")
        try:
            amount = float(self.io_interface.input("Amount to deposit: "))
            self.atm.deposit(account_id=acc_num, amount=amount)
            self.io_interface.print(f"Deposited {amount} to account {acc_num}.")
        except ATMError as e:
            self.io_interface.print(f"Deposit failed: {e}")

    def handle_transfer(self):
        from_acc = self.io_interface.input("From account number: ")
        to_acc = self.io_interface.input("To account number: ")
        try:
            amount = float(self.io_interface.input("Amount to transfer: "))
            self.atm.transfer(from_acc, to_acc, amount)
            self.io_interface.print(f"Transferred {amount} from account {from_acc} to account {to_acc}.")
        except ATMError as e:
            self.io_interface.print(f"Transfer failed: {e}")

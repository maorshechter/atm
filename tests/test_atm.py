import pytest
from typing import Dict
from src.atm import ATM
from dao import User, Password, Account
from exceptions import UnauthorizedAccessError, InvalidAmountError, AccountNotFoundError


@pytest.fixture
def atm() -> ATM:
    users: Dict[str, User] = {
        "user1": User(user_id="user1", name="John Doe"),
        "user2": User(user_id="user2", name="Jane Smith"),
    }
    passwords: Dict[str, Password] = {
        "user1": Password(user_id="user1", password="password123"),
        "user2": Password(user_id="user2", password="securepass"),
    }
    accounts: Dict[str, Account] = {
        "acc1": Account(account_id="acc1", owner_id="user1", balance=100.0),
        "acc2": Account(account_id="acc2", owner_id="user2", balance=200.0),
    }
    return ATM(users, passwords, accounts)


def test_authenticate_success(atm: ATM) -> None:
    assert atm.authenticate("user1", "password123") == "John Doe"


def test_authenticate_invalid_password(atm: ATM) -> None:
    with pytest.raises(UnauthorizedAccessError):
        atm.authenticate("user1", "wrongpassword")


def test_authenticate_nonexistent_user(atm: ATM) -> None:
    with pytest.raises(UnauthorizedAccessError):
        atm.authenticate("nonexistent_user", "password123")


def test_get_balance_success(atm: ATM) -> None:
    atm.authenticate("user1", "password123")
    assert atm.get_balance() == {"acc1": 100.0}


def test_get_balance_without_authentication(atm: ATM) -> None:
    with pytest.raises(UnauthorizedAccessError):
        atm.get_balance()


def test_withdraw_success(atm: ATM) -> None:
    atm.authenticate("user1", "password123")
    atm.withdraw("acc1", 50.0)
    assert atm.accounts["acc1"].balance == 50.0


def test_withdraw_invalid_amount(atm: ATM) -> None:
    atm.authenticate("user1", "password123")
    with pytest.raises(InvalidAmountError):
        atm.withdraw("acc1", -50.0)


def test_withdraw_without_authentication(atm: ATM) -> None:
    with pytest.raises(UnauthorizedAccessError):
        atm.withdraw("acc1", 50.0)


def test_transfer_success(atm: ATM) -> None:
    atm.authenticate("user1", "password123")
    atm.transfer("acc1", "acc2", 50.0)
    assert atm.accounts["acc1"].balance == 50.0
    assert atm.accounts["acc2"].balance == 250.0


def test_transfer_to_nonexistent_account(atm: ATM) -> None:
    atm.authenticate("user1", "password123")
    with pytest.raises(AccountNotFoundError):
        atm.transfer("acc1", "nonexistent_acc", 50.0)


def test_transfer_without_authentication(atm: ATM) -> None:
    with pytest.raises(UnauthorizedAccessError):
        atm.transfer("acc1", "acc2", 50.0)


def test_deposit_success(atm: ATM) -> None:
    atm.authenticate("user1", "password123")
    atm.deposit("acc1", 50.0)
    assert atm.accounts["acc1"].balance == 150.0


def test_deposit_negative_amount(atm: ATM) -> None:
    atm.authenticate("user1", "password123")
    with pytest.raises(InvalidAmountError):
        atm.deposit("acc1", -50.0)


def test_deposit_to_nonexistent_account(atm: ATM) -> None:
    atm.authenticate("user1", "password123")
    with pytest.raises(AccountNotFoundError):
        atm.deposit("nonexistent_acc", 50.0)


def test_deposit_unauthorized_access(atm: ATM) -> None:
    atm.authenticate("user1", "password123")
    with pytest.raises(UnauthorizedAccessError):
        atm.deposit("acc2", 50.0)


def test_deposit_without_authentication(atm: ATM) -> None:
    with pytest.raises(UnauthorizedAccessError):
        atm.deposit("acc1", 50.0)


def test_change_password_success(atm: ATM) -> None:
    atm.authenticate("user1", "password123")
    atm.change_password("newpassword123")
    assert atm.passwords["user1"].password == "newpassword123"


def test_change_password_without_authentication(atm: ATM) -> None:
    with pytest.raises(UnauthorizedAccessError):
        atm.change_password("newpassword123")

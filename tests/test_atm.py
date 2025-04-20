import pytest
from typing import Dict, Any
from src.atm import ATM
from exceptions import UnauthorizedAccessError, InvalidAmountError, AccountNotFoundError


@pytest.fixture
def atm() -> ATM:
    users: Dict[str, Dict[str, str]] = {
        "user1": {"name": "John Doe"},
        "user2": {"name": "Jane Smith"}
    }
    passwords: Dict[str, Dict[str, str]] = {
        "user1": {"password": "password123"},
        "user2": {"password": "securepass"}
    }
    accounts: Dict[str, Dict[str, Any]] = {
        "acc1": {"owner_id": "user1", "balance": 100.0},
        "acc2": {"owner_id": "user2", "balance": 200.0}
    }
    return ATM(users, passwords, accounts)


def test_authenticate_success(atm: ATM) -> None:
    assert atm.authenticate("user1", "password123") == "John Doe"


def test_authenticate_invalid_password(atm: ATM) -> None:
    with pytest.raises(UnauthorizedAccessError, match="Authentication failed: Invalid username or password."):
        atm.authenticate("user1", "wrongpassword")


def test_authenticate_nonexistent_user(atm: ATM) -> None:
    with pytest.raises(UnauthorizedAccessError, match="Authentication failed: Invalid username or password."):
        atm.authenticate("nonexistent_user", "password123")


def test_get_balance_success(atm: ATM) -> None:
    atm.authenticate("user1", "password123")
    assert atm.get_balance() == {"acc1": 100.0}


def test_get_balance_without_authentication(atm: ATM) -> None:
    with pytest.raises(UnauthorizedAccessError, match="Operation not allowed: User must be authenticated."):
        atm.get_balance()


def test_withdraw_success(atm: ATM) -> None:
    atm.authenticate("user1", "password123")
    atm.withdraw("acc1", 50.0)
    assert atm.accounts["acc1"]["balance"] == 50.0


def test_withdraw_invalid_amount(atm: ATM) -> None:
    atm.authenticate("user1", "password123")
    with pytest.raises(InvalidAmountError, match="Withdrawal failed: Amount must be positive."):
        atm.withdraw("acc1", -50.0)


def test_withdraw_without_authentication(atm: ATM) -> None:
    with pytest.raises(UnauthorizedAccessError, match="Operation not allowed: User must be authenticated."):
        atm.withdraw("acc1", 50.0)


def test_transfer_success(atm: ATM) -> None:
    atm.authenticate("user1", "password123")
    atm.transfer("acc1", "acc2", 50.0)
    assert atm.accounts["acc1"]["balance"] == 50.0
    assert atm.accounts["acc2"]["balance"] == 250.0


def test_transfer_to_nonexistent_account(atm: ATM) -> None:
    atm.authenticate("user1", "password123")
    with pytest.raises(AccountNotFoundError, match="Transfer failed: To account not found."):
        atm.transfer("acc1", "nonexistent_acc", 50.0)


def test_transfer_without_authentication(atm: ATM) -> None:
    with pytest.raises(UnauthorizedAccessError, match="Operation not allowed: User must be authenticated."):
        atm.transfer("acc1", "acc2", 50.0)


def test_deposit_success(atm: ATM) -> None:
    atm.authenticate("user1", "password123")
    atm.deposit("acc1", 50.0)
    assert atm.accounts["acc1"]["balance"] == 150.0


def test_deposit_negative_amount(atm: ATM) -> None:
    atm.authenticate("user1", "password123")
    with pytest.raises(InvalidAmountError, match="Deposit failed: Amount must be positive."):
        atm.deposit("acc1", -50.0)


def test_deposit_to_nonexistent_account(atm: ATM) -> None:
    atm.authenticate("user1", "password123")
    with pytest.raises(AccountNotFoundError, match="Deposit failed: Account not found."):
        atm.deposit("nonexistent_acc", 50.0)


def test_deposit_unauthorized_access(atm: ATM) -> None:
    atm.authenticate("user1", "password123")
    with pytest.raises(UnauthorizedAccessError, match="Deposit failed: Unauthorized access."):
        atm.deposit("acc2", 50.0)


def test_deposit_without_authentication(atm: ATM) -> None:
    with pytest.raises(UnauthorizedAccessError, match="Operation not allowed: User must be authenticated."):
        atm.deposit("acc1", 50.0)


def test_change_password_success(atm: ATM) -> None:
    atm.authenticate("user1", "password123")
    atm.change_password("newpassword123")
    assert atm.passwords["user1"]["password"] == "newpassword123"


def test_change_password_without_authentication(atm: ATM) -> None:
    with pytest.raises(UnauthorizedAccessError, match="Operation not allowed: User must be authenticated."):
        atm.change_password("newpassword123")

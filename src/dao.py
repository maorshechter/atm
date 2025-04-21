from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class User:
    user_id: str
    name: str
    email: str = ""

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "User":
        return User(user_id=data.get("user_id", ""), name=data.get("name", ""), email=data.get("email", ""))

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Password:
    user_id: str
    password: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Password":
        return Password(user_id=data["user_id"], password=data["password"])

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Account:
    owner_id: str
    balance: float
    account_id: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Account":
        return Account(
            owner_id=data["owner_id"],
            balance=float(data["balance"]),
            account_id=data["account_id"]
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

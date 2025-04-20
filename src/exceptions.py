class ATMError(Exception):
    pass


class UnauthorizedAccessError(ATMError):
    pass


class AccountNotFoundError(ATMError):
    pass


class InvalidAmountError(ATMError):
    pass



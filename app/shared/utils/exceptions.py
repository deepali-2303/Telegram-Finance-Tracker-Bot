class FinanceTrackerError(Exception):
    """Base exception for all finance tracker errors."""

    default_message = "An unexpected finance tracker error occurred."

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)


class ParseError(FinanceTrackerError):
    default_message = "Could not parse the message."


class InsufficientBalanceError(FinanceTrackerError):
    default_message = "Insufficient balance for this transaction."


class CategoryNotFoundError(FinanceTrackerError):
    default_message = "Category does not exist."


class TransactionNotFoundError(FinanceTrackerError):
    default_message = "Transaction not found."


class LimitNotSetError(FinanceTrackerError):
    default_message = "Monthly limit is not configured."


class DatabaseError(FinanceTrackerError):
    default_message = "A database error occurred."

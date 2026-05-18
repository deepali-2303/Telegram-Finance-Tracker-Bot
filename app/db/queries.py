import sqlite3
from typing import Optional

from app.shared.db_queries.config_queries import (
    INSERT_CONFIG_VALUE,
    SELECT_CONFIG_ALL,
    SELECT_CONFIG_VALUE,
)
from app.shared.db_queries.transcation_queries import (
    DELETE_TRANSACTION_QUERY,
    INSERT_TRANSACTION_QUERY,
    SELECT_CATEGORY_TOTALS_BY_MONTH_QUERY,
    SELECT_LAST_TRANSACTIONS_QUERY,
    SELECT_MONTH_TRANSACTIONS_QUERY,
    SELECT_TODAY_TRANSACTIONS_QUERY,
)
from app.shared.utils.exceptions import DatabaseError


def config_get(conn: sqlite3.Connection, key: str) -> Optional[str]:
    """
    Fetch a configuration value by key from the system_config table.
    Params:
        conn: An active SQLite connection.
        key: The configuration key to look up.
    Returns:
        The configuration value as a string, or None if the key does not exist.
    """
    try:
        row = conn.execute(SELECT_CONFIG_VALUE, (key,)).fetchone()
        return row["value"] if row else None
    except sqlite3.Error as e:
        raise DatabaseError(
            f"Database error while fetching config for key '{key}': {e}"
        )


def config_set(conn: sqlite3.Connection, key: str, value: str) -> None:
    """
    Insert or update a configuration key-value pair in the system_config table.
    Params:
        conn: An active SQLite connection.
        key: The configuration key to set.
        value: The configuration value to set.
    Returns:
        None
    """
    try:
        conn.execute(INSERT_CONFIG_VALUE, (key, value))
        conn.commit()
    except sqlite3.Error as e:
        raise DatabaseError(f"Database error while setting config for key '{key}': {e}")


def config_get_all(conn: sqlite3.Connection) -> list[dict]:
    """Fetch all configuration key-value pairs from the system_config table.
    Params:
        conn: An active SQLite connection.
    Returns:
        A list of dictionaries, each containing 'key', 'value', 'description', and 'updated_at' for each configuration entry.
    """
    try:
        rows = conn.execute(SELECT_CONFIG_ALL).fetchall()
        return [dict(r) for r in rows]
    except sqlite3.Error as e:
        raise DatabaseError(f"Database error while fetching all config: {e}")


def txn_insert(
    conn: sqlite3.Connection,
    type: str,
    category: str,
    amount: float,
    account: str,
    note: Optional[str] = None,
) -> int | None:
    """Insert a new transaction into the transactions table.
    Params:
        conn: An active SQLite connection.
        type: The transaction type, either 'debit' or 'credit'.
        category: The transaction category.
        amount: The transaction amount (must be > 0).
        account: The account involved in the transaction, either 'gpayWallet' or 'bank'.
        note: An optional note about the transaction.
    Returns:
        The ID of the newly inserted transaction, or None if the operation failed.
    """
    cur = None
    try:
        cur = conn.execute(
            INSERT_TRANSACTION_QUERY,
            (type, category, amount, account, note),
        )
        conn.commit()
    except sqlite3.Error as e:
        raise DatabaseError(f"Database error while inserting transaction: {e}")
    return cur.lastrowid if cur else None


def txn_delete(conn: sqlite3.Connection, txn_id: int) -> bool:
    """
    Delete a transaction from the transactions table by its ID.
    Params:
        conn: An active SQLite connection.
        txn_id: The ID of the transaction to delete.
    Returns:
        True if a transaction was deleted, False if no transaction with the given ID was found.
    """
    try:
        cur = conn.execute(DELETE_TRANSACTION_QUERY, (txn_id,))
        conn.commit()
        return cur.rowcount > 0
    except sqlite3.Error as e:
        raise DatabaseError(
            f"Database error while deleting transaction with id {txn_id}: {e}"
        )


def txn_get_last(conn: sqlite3.Connection, n: int = 1) -> list[dict]:
    """
    Fetch the last n transactions from the transactions table, ordered by most recent first.
    Params:
        conn: An active SQLite connection.
        n: The number of recent transactions to fetch (default is 1).
    Returns:
        A list of dictionaries, each representing a transaction record.
    """
    try:
        rows = conn.execute(SELECT_LAST_TRANSACTIONS_QUERY, (n,)).fetchall()
        return [dict(r) for r in rows]
    except sqlite3.Error as e:
        raise DatabaseError(f"Database error while fetching last {n} transactions: {e}")


def txn_get_today(conn: sqlite3.Connection) -> list[dict]:
    """
    Fetch all transactions from the transactions table that were created today, ordered by most recent first.
    Params:
        conn: An active SQLite connection.
    Returns:
        A list of dictionaries, each representing a transaction record created today.
    """
    try:
        rows = conn.execute(SELECT_TODAY_TRANSACTIONS_QUERY).fetchall()
        return [dict(r) for r in rows]
    except sqlite3.Error as e:
        raise DatabaseError(f"Database error while fetching today's transactions: {e}")


def txn_get_by_month(conn: sqlite3.Connection, month: str) -> list[dict]:
    """Fetch all transactions from the transactions table for a given month, ordered by most recent first.
    Params:
        conn: An active SQLite connection.
        month: The month for which to fetch transactions (format: 'YYYY-MM').
    Returns:
        A list of dictionaries, each representing a transaction record for the specified month.
    """
    try:
        rows = conn.execute(
            SELECT_MONTH_TRANSACTIONS_QUERY,
            (month,),
        ).fetchall()
        return [dict(r) for r in rows]
    except sqlite3.Error as e:
        raise DatabaseError(
            f"Database error while fetching transactions for month {month}: {e}"
        )


def txn_category_totals_by_month(conn: sqlite3.Connection, month: str) -> list[dict]:
    """
    Fetch total amounts and counts of 'expense' transactions grouped by category for a given month.
    Params:
        conn: An active SQLite connection.
        month: The month for which to fetch category totals (format: 'YYYY-MM').
    Returns:
        A list of dictionaries, each containing 'category', 'total', and 'count' for each expense category in the specified month.
    """
    try:
        rows = conn.execute(
            SELECT_CATEGORY_TOTALS_BY_MONTH_QUERY,
            (month,),
        ).fetchall()
        return [dict(r) for r in rows]
    except sqlite3.Error as e:
        raise DatabaseError(
            f"Database error while fetching category totals for month {month}: {e}"
        )

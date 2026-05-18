INSERT_TRANSACTION_QUERY = """
        INSERT INTO transactions (type, category, amount, account, note)
        VALUES (?, ?, ?, ?, ?)
    """
DELETE_TRANSACTION_QUERY = "DELETE FROM transactions WHERE id = ?"

SELECT_LAST_TRANSACTIONS_QUERY = "SELECT * FROM transactions ORDER BY id DESC LIMIT ?"

SELECT_TODAY_TRANSACTIONS_QUERY = """
            SELECT * FROM transactions
            WHERE date(created_at) = date('now', 'localtime')
            ORDER BY id
        """
SELECT_MONTH_TRANSACTIONS_QUERY = """
            SELECT * FROM transactions
            WHERE strftime('%Y-%m', created_at) = ?
            ORDER BY id
        """

SELECT_CATEGORY_TOTALS_BY_MONTH_QUERY = """
            SELECT   category,
                     SUM(amount)  AS total,
                     COUNT(*)     AS count
            FROM     transactions
            WHERE    type = 'expense'
              AND    strftime('%Y-%m', created_at) = ?
            GROUP BY category
            ORDER BY total DESC
        """

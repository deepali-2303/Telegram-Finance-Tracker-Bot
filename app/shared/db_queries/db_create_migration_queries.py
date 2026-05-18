initialCreateTablesQuery = """
        CREATE TABLE IF NOT EXISTS transactions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            type        TEXT    NOT NULL CHECK (type IN ('debit', 'credit')),
            category    TEXT    NOT NULL,
            amount      REAL    NOT NULL CHECK (amount > 0),
            account     TEXT    NOT NULL CHECK (account IN ('gpayWallet', 'bank')),
            note        TEXT,
            created_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
        );

        CREATE INDEX IF NOT EXISTS idx_txn_created_at ON transactions (created_at);
        CREATE INDEX IF NOT EXISTS idx_txn_category   ON transactions (category);
        CREATE INDEX IF NOT EXISTS idx_txn_type       ON transactions (type);

        CREATE TABLE IF NOT EXISTS system_config (
            key         TEXT PRIMARY KEY,
            value       TEXT NOT NULL,
            description TEXT,
            updated_at  TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        );

        INSERT OR IGNORE INTO system_config (key, value, description) VALUES
            ('gpay_wallet_balance',         '0.0',    'Current GPay wallet balance'),
            ('bank_balance',                '0.0',    'Current bank account balance'),
            ('gpay_wallet_alert_threshold', '100.0',  'Alert threshold for low GPay wallet balance'),
            ('bank_alert_threshold',        '2000.0', 'Alert threshold for low bank balance');

        CREATE TABLE IF NOT EXISTS category_limits (
            category      TEXT  PRIMARY KEY,
            monthly_limit REAL  NOT NULL CHECK (monthly_limit > 0),
            description   TEXT,
            updated_at    TEXT  NOT NULL DEFAULT (datetime('now', 'localtime'))
        );
        """


schemaMigrationsQuery = """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version    INTEGER PRIMARY KEY,
                applied_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
            )
        """

selectMigrationsQuery = """SELECT version FROM schema_migrations"""


insertMigrationQuery = """
    INSERT INTO schema_migrations (version) VALUES (?)
"""

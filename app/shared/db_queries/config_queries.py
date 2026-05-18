SELECT_CONFIG_VALUE = "SELECT value FROM system_config WHERE key = ?"
INSERT_CONFIG_VALUE = """
        INSERT INTO system_config (key, value, updated_at)
        VALUES (?, ?, datetime('now', 'localtime'))
        ON CONFLICT(key) DO UPDATE SET
            value      = excluded.value,
            updated_at = excluded.updated_at
    """
SELECT_CONFIG_ALL = (
    """SELECT key, value, description, updated_at FROM system_config ORDER BY key"""
)

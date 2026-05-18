import sqlite3
import logging
from pathlib import Path
from shared.utils.exceptions import DatabaseError
from app.shared.db_queries.db_create_migration_queries import (
    initialCreateTablesQuery,
    schemaMigrationsQuery,
    selectMigrationsQuery,
    insertMigrationQuery,
)

logger = logging.getLogger(__name__)

MIGRATIONS = [
    (
        1,
        "create transactions, system_config, and category_limits tables",
        initialCreateTablesQuery,
    ),
]


def get_connection(db_path: str = "data/finance.db") -> sqlite3.Connection:
    """
    Get a SQLite connection to the specified database path. Creates the parent directory if it doesn't exist.
    Params:
        db_path (str): The file path to the SQLite database. Defaults to "data/finance.db".
    Returns:
        sqlite3.Connection: A connection object to the SQLite database.
    """
    conn = None
    try:
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(
            db_path,
            check_same_thread=False,
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}")
        raise DatabaseError(f"Failed to connect to database: {e}")
    return conn


def run_migrations(conn: sqlite3.Connection) -> None:
    """
    Run database migrations to ensure the schema is up to date. Creates a schema_migrations table to track applied migrations.
    Params:
        conn (sqlite3.Connection): An active connection to the SQLite database.
    Returns:
        None
    """
    try:
        conn.execute(schemaMigrationsQuery)
        conn.commit()

        applied = {row[0] for row in conn.execute(selectMigrationsQuery).fetchall()}

        for version, description, sql in MIGRATIONS:
            if version in applied:
                continue
            logger.info(f"Applying migration v{version}: {description}")
            conn.executescript(sql)
            conn.execute(insertMigrationQuery, (version,))
            conn.commit()
            logger.info(f"Migration v{version} done")
    except sqlite3.Error as e:
        logger.error(f"Error running migrations: {e}")
        raise DatabaseError(f"Failed to run migrations: {e}")


def init_db(db_path: str = "data/finance.db") -> sqlite3.Connection:
    """
    Initialize the database by getting a connection and running migrations.
    Params:
        db_path (str): The file path to the SQLite database. Defaults to "data/finance.db".
    Returns:
        sqlite3.Connection: A connection object to the initialized SQLite database.
    """
    conn = get_connection(db_path)
    run_migrations(conn)
    return conn

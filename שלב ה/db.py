"""
Database connection module.
Handles all PostgreSQL connections using psycopg2.

IMPORTANT: Update the DB_CONFIG below with YOUR database credentials before running!
"""

import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

# ============================================================
# UPDATE THESE WITH YOUR DATABASE CREDENTIALS
# ============================================================
DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "database": "hospital_db",   # <-- your DB name
    "user": "gitty_user",          # <-- your username
    "password": "GittyPass123"  # <-- your password
}
# ============================================================


def get_connection():
    """Open a new connection to the database."""
    return psycopg2.connect(**DB_CONFIG)


def run_query(query, params=None, fetch=True):
    """
    Run a SELECT query and return list of dicts.
    Use for read operations.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, params or ())
        if fetch:
            rows = cur.fetchall()
            return [dict(r) for r in rows]
        return None
    finally:
        if conn:
            conn.close()


def run_action(query, params=None):
    """
    Run an INSERT/UPDATE/DELETE query.
    Returns number of affected rows.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, params or ())
        affected = cur.rowcount
        conn.commit()
        return affected
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


def call_function(func_name, params=None):
    """
    Call a PL/pgSQL function and return its result.
    Example: call_function('get_underutilized_staff', (1,))
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        placeholders = ",".join(["%s"] * len(params)) if params else ""
        query = f"SELECT * FROM {func_name}({placeholders})"
        cur.execute(query, params or ())
        try:
            rows = cur.fetchall()
            return [dict(r) for r in rows]
        except psycopg2.ProgrammingError:
            return None
    finally:
        if conn:
            conn.close()


def call_procedure(proc_name, params=None):
    """
    Call a PL/pgSQL procedure (CALL syntax).
    Example: call_procedure('transfer_patient', (1, 5, 10))
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        placeholders = ",".join(["%s"] * len(params)) if params else ""
        query = f"CALL {proc_name}({placeholders})"
        cur.execute(query, params or ())
        conn.commit()
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


def test_connection():
    """Quick health check - call this from your main file at startup."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        conn.close()
        return True, version[0]
    except Exception as e:
        return False, str(e)

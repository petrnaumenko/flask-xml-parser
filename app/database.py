import sqlite3
from contextlib import contextmanager
from flask import current_app
import os


@contextmanager
def get_db_connection():
    """Контекстный менеджер для подключения к базе данных."""
    db_path = current_app.config.get('DATABASE')
    if not db_path:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(BASE_DIR, 'instance', 'database.db')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Возвращать результаты в виде словаря
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def get_db_cursor():
    """Контекстный менеджер для работы с курсором."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
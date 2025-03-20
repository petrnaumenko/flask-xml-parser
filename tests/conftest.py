import pytest
import os
import sqlite3
from flask import Flask
from app.routes.file_routes import file_bp
from app.routes.tag_routes import tag_bp

TEST_DATABASE = "test_database.db"


def pytest_addoption(parser):
    """Добавляем параметр --log для контроля вывода логов в тестах."""
    parser.addoption(
        "--log", action="store_true", default=False, help="Enable logging output"
    )


@pytest.fixture(scope="module")
def setup_database(request):
    """Фикстура для создания тестовой базы данных."""    
    log_param = request.config.getoption("--log")
    
    if os.path.exists(TEST_DATABASE):
        os.remove(TEST_DATABASE)

    with sqlite3.connect(TEST_DATABASE) as conn:
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'migrations', 'init_db.sql')
        with open(file_path, "r") as f:
            sql_script = f.read()
            conn.executescript(sql_script)
        
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if log_param:
            print(f"Таблицы в базе данных: {tables}")

    yield TEST_DATABASE

    if os.path.exists(TEST_DATABASE):
        os.remove(TEST_DATABASE)


@pytest.fixture
def db_cursor(setup_database):
    """Фикстура для получения курсора тестовой базы данных."""    
    conn = sqlite3.connect(setup_database)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    yield cursor
    conn.close()


@pytest.fixture
def client(setup_database, request):
    """Фикстура для создания тестового клиента Flask."""    
    log_param = request.config.getoption("--log")

    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['DATABASE'] = setup_database
    app.register_blueprint(file_bp)
    app.register_blueprint(tag_bp)
    
    with app.app_context():
        if log_param:
            print("Создание тестового клиента Flask.")
        yield app.test_client()
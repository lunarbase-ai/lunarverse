import sqlite3
import pytest
from sqlite_query import SqliteQuery


@pytest.fixture
def sqlite_db_path(tmp_path):
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)"
    )
    cursor.executemany(
        "INSERT INTO users (name, age) VALUES (?, ?)",
        [
            ("Alice", 30),
            ("Bob", 25),
        ],
    )
    conn.commit()
    conn.close()
    return str(db_path)


@pytest.fixture
def component():
    return SqliteQuery()


def test_run_success(component, sqlite_db_path):
    query = "SELECT * FROM users ORDER BY id"
    result = component.run(db_path=sqlite_db_path, query=query)
    assert "id,name,age" in result
    assert "1,Alice,30" in result
    assert "2,Bob,25" in result


def test_run_invalid_sql(component, sqlite_db_path):
    query = "SELECT * FROM non_existing_table"
    result = component.run(db_path=sqlite_db_path, query=query)
    assert "no such table" in result.lower()


def test_run_invalid_db_path(tmp_path, component):
    db_path = str(tmp_path / "does_not_exist.db")
    result = component.run(db_path=db_path, query="SELECT * FROM users")
    assert (
        "no such table" in result.lower()
        or "unable to open database file" in result.lower()
    )

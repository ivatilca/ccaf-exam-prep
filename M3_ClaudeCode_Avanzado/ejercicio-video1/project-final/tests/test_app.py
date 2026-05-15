import pytest
import sqlite3
from unittest.mock import patch
from demo import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def make_db_with_missions(count=0):
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    conn.execute('CREATE TABLE missions (id INTEGER PRIMARY KEY, name TEXT)')
    for i in range(count):
        conn.execute('INSERT INTO missions (name) VALUES (?)', (f'Mission {i + 1}',))
    conn.commit()
    return conn


def test_health_returns_ok(client):
    db = make_db_with_missions(count=0)
    with patch('demo.get_db', return_value=db):
        response = client.get('/health')
    assert response.status_code == 200
    body = response.get_json()
    assert body['error'] is None
    assert body['data']['status'] == 'ok'
    assert body['data']['missions'] == 0


def test_health_reflects_mission_count(client):
    db = make_db_with_missions(count=3)
    with patch('demo.get_db', return_value=db):
        response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['data']['missions'] == 3

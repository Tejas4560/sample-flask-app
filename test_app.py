"""
Basic tests for Flask Task Manager API
"""

import pytest
from app import app


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'running'


def test_get_tasks_empty(client):
    """Test getting tasks when none exist"""
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert 'tasks' in data


def test_create_task(client):
    """Test creating a new task"""
    response = client.post('/api/tasks', json={
        'title': 'Test Task',
        'description': 'This is a test task'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Test Task'
    assert data['completed'] == False


def test_create_task_without_title(client):
    """Test creating task without title fails"""
    response = client.post('/api/tasks', json={
        'description': 'No title'
    })
    assert response.status_code == 400

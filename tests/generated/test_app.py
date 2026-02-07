"""Tests for app module."""

import sys
import os
import pytest
from app import app  # Ensure the real app is imported for testing

sys.path.insert(0, r"/home/runner/work/sample-flask-app/sample-flask-app/pipeline/target_repo")
def client():
    with app.test_client() as client:
        yield client


class TestAppIntegration:
    """Integration tests for app."""

    def test_health_check_success(self, client):
        """UNIVERSAL test for maximum coverage."""
        """Test the health check endpoint."""
        response = client.get('/')
        assert response.status_code == 200
        data = response.get_json()
        assert data is not None
        assert 'status' in data
        assert data['status'] == 'running'
        assert 'message' in data
        assert 'timestamp' in data

    def test_get_tasks_empty(self, client):
        """UNIVERSAL test for maximum coverage."""
        """Test that an empty task list is returned initially."""
        response = client.get('/api/tasks')
        assert response.status_code == 200
        data = response.get_json()
        assert 'tasks' in data
        assert isinstance(data['tasks'], list)
        assert len(data['tasks']) == 0

    def test_create_task_success(self, client):
        """UNIVERSAL test for maximum coverage."""
        """Test successful creation of a new task."""
        response = client.post('/api/tasks', json={'title': 'Test Task', 'description': 'This is a test task.'})
        assert response.status_code == 201
        data = response.get_json()
        assert 'id' in data and data['id'] is not None
        assert 'title' in data and data['title'] == 'Test Task'
        assert 'description' in data and data['description'] == 'This is a test task.'
        assert 'completed' in data and not data['completed']
        assert 'created_at' in data

    def test_create_task_missing_title(self, client):
        """UNIVERSAL test for maximum coverage."""
        """Test creation of a task with a missing title."""
        response = client.post('/api/tasks', json={'description': 'This task has no title.'})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_get_task_success(self, client):
        """UNIVERSAL test for maximum coverage."""
        """Test retrieving a specific task."""
        create_response = client.post('/api/tasks', json={'title': 'Sample Task', 'description': 'Task details'})
        task_id = create_response.get_json()['id']
        response = client.get(f'/api/tasks/{task_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert 'id' in data and data['id'] == task_id
        assert 'title' in data and data['title'] == 'Sample Task'

    def test_get_task_not_found(self, client):
        """UNIVERSAL test for maximum coverage."""
        """Test retrieving a task that doesn't exist."""
        response = client.get('/api/tasks/999')
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data

    def test_update_task_success(self, client):
        """UNIVERSAL test for maximum coverage."""
        """Test successfully updating a task."""
        create_response = client.post('/api/tasks', json={'title': 'Task to Update'})
        task_id = create_response.get_json()['id']
        response = client.put(f'/api/tasks/{task_id}', json={'title': 'Updated Task', 'completed': True})
        assert response.status_code == 200
        data = response.get_json()
        assert 'title' in data and data['title'] == 'Updated Task'
        assert 'completed' in data and data['completed']

    def test_update_task_not_found(self, client):
        """UNIVERSAL test for maximum coverage."""
        """Test updating a task that doesn't exist."""
        response = client.put('/api/tasks/999', json={'title': 'Nonexistent Task'})
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data

    def test_delete_task_success(self, client):
        """UNIVERSAL test for maximum coverage."""
        """Test successfully deleting a task."""
        create_response = client.post('/api/tasks', json={'title': 'Task to Delete'})
        task_id = create_response.get_json()['id']
        response = client.delete(f'/api/tasks/{task_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data

        # Verify task no longer exists
        get_response = client.get(f'/api/tasks/{task_id}')
        assert get_response.status_code == 404

    def test_delete_task_not_found(self, client):
        """UNIVERSAL test for maximum coverage."""
        """Test deleting a task that doesn't exist."""
        response = client.delete('/api/tasks/999')
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data

    def test_register_user_success(self, client):
        """UNIVERSAL test for maximum coverage."""
        """Test successful user registration."""
        response = client.post('/api/auth/register', json={'username': 'testuser', 'password': 'password123'})
        assert response.status_code == 201
        data = response.get_json()
        assert 'id' in data and data['id'] is not None
        assert 'username' in data and data['username'] == 'testuser'

    def test_register_user_missing_fields(self, client):
        """UNIVERSAL test for maximum coverage."""
        """Test user registration with missing fields."""
        response = client.post('/api/auth/register', json={'username': 'testuser'})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_register_user_duplicate(self, client):
        """UNIVERSAL test for maximum coverage."""
        """Test registering a user with a duplicate username."""
        client.post('/api/auth/register', json={'username': 'duplicateuser', 'password': 'password123'})
        response = client.post('/api/auth/register', json={'username': 'duplicateuser', 'password': 'password123'})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_login_success(self, client):
        """UNIVERSAL test for maximum coverage."""
        """Test successful user login."""
        client.post('/api/auth/register', json={'username': 'testuser', 'password': 'password123'})
        response = client.post('/api/auth/login', json={'username': 'testuser', 'password': 'password123'})
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data
        assert 'user' in data and 'id' in data['user'] and 'username' in data['user']

    def test_login_invalid_credentials(self, client):
        """UNIVERSAL test for maximum coverage."""
        """Test login with invalid credentials."""
        client.post('/api/auth/register', json={'username': 'testuser', 'password': 'password123'})
        response = client.post('/api/auth/login', json={'username': 'testuser', 'password': 'wrongpassword'})
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data


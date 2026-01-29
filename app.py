"""
Simple Flask Task Manager API
"""

from flask import Flask, jsonify, request
from datetime import datetime

print("hELLOOOOOOOOOOOO")    
app = Flask(__name__)

# In-memory storage for tasks
tasks = []
users = []
task_id_counter = 1
user_id_counter = 1


@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'message': 'Task Manager API is running',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    return jsonify({'tasks': tasks})


@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    global task_id_counter
    
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    task = {
        'id': task_id_counter,
        'title': data['title'],
        'description': data.get('description', ''),
        'completed': False,
        'created_at': datetime.now().isoformat()
    }
    
    tasks.append(task)
    task_id_counter += 1
    
    return jsonify(task), 201


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(task)


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    
    if 'title' in data:
        task['title'] = data['title']
    if 'description' in data:
        task['description'] = data['description']
    if 'completed' in data:
        task['completed'] = data['completed']
    
    task['updated_at'] = datetime.now().isoformat()
    
    return jsonify(task)


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    global tasks
    
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    tasks = [t for t in tasks if t['id'] != task_id]
    
    return jsonify({'message': 'Task deleted successfully'})


@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    global user_id_counter
    
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password are required'}), 400
    
    # Check if user already exists
    if any(u['username'] == data['username'] for u in users):
        return jsonify({'error': 'User already exists'}), 400
    
    user = {
        'id': user_id_counter,
        'username': data['username'],
        'password': data['password'],  # In production, hash this!
        'created_at': datetime.now().isoformat()
    }
    
    users.append(user)
    user_id_counter += 1
    
    return jsonify({'id': user['id'], 'username': user['username']}), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password are required'}), 400
    
    user = next((u for u in users if u['username'] == data['username'] and u['password'] == data['password']), None)
    
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    return jsonify({
        'message': 'Login successful',
        'user': {'id': user['id'], 'username': user['username']}
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)

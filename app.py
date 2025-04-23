from flask import Flask, request, jsonify, render_template
from models import db, Task
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# Root route for HTML page or JSON welcome message
@app.route('/', methods=['GET'])
def home():
    try:
        return render_template('index.html')
    except:
        return jsonify({
            'message': 'Welcome to the Task Manager API!',
            'endpoints': {
                'POST /tasks': 'Create a new task',
                'GET /tasks': 'List all tasks',
                'GET /tasks/<id>': 'Get a specific task',
                'PUT /tasks/<id>': 'Update a task',
                'DELETE /tasks/<id>': 'Delete a task',
                'GET /tasks/filter': 'Filter tasks by status or priority'
            }
        }), 200

# Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Task name is required'}), 400
    
    task = Task(
        name=data['name'],
        description=data.get('description'),
        status=data.get('status', 'running'),
        priority=min(max(data.get('priority', 1), 1), 5)
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

# List all tasks
@app.route('/tasks', methods=['GET'])
def list_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks]), 200

# Get a specific task
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify(task.to_dict()), 200

# Update a task
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    
    task.name = data.get('name', task.name)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    task.priority = min(max(data.get('priority', task.priority), 1), 5)
    
    db.session.commit()
    return jsonify(task.to_dict()), 200

# Delete a task
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'}), 200

# Filter tasks by status or priority
@app.route('/tasks/filter', methods=['GET'])
def filter_tasks():
    status = request.args.get('status')
    priority = request.args.get('priority', type=int)
    
    query = Task.query
    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    
    tasks = query.all()
    return jsonify([task.to_dict() for task in tasks]), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
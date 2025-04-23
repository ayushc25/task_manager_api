Task Manager API
A Unix-inspired RESTful API for managing tasks, built with Flask and SQLite.
Setup

Clone the repository:
git clone <repository-url>
cd task_manager_api


Create and activate a virtual environment:
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate


Install dependencies:
pip install -r requirements.txt


Run the application:
python app.py



The API will be available at http://127.0.0.1:5000.
API Endpoints

POST /tasks

Create a new task.
Request body:{
    "name": "Task name",
    "description": "Task description",
    "status": "running",
    "priority": 3
}


Response: Task object (201)


GET /tasks

List all tasks.
Response: Array of task objects (200)


GET /tasks/

Get a specific task by ID.
Response: Task object (200) or 404 if not found


PUT /tasks/

Update a task.
Request body: Same as POST, fields are optional.
Response: Updated task object (200) or 404


DELETE /tasks/

Delete a task.
Response: { "message": "Task deleted" } (200) or 404


GET /tasks/filter?status=&priority=

Filter tasks by status and/or priority.
Response: Array of matching task objects (200)



Example Usage
Create a task:
curl -X POST http://127.0.0.1:5000/tasks \
-H "Content-Type: application/json" \
-d '{"name":"Write report","description":"Draft quarterly report","priority":3}'

List tasks:
curl http://127.0.0.1:5000/tasks

Dependencies

Flask
Flask-SQLAlchemy
Marshmallow (optional, for validation)

Install via:
pip install -r requirements.txt


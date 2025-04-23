from flask_mongoengine import MongoEngine

db = MongoEngine()

class Task(db.Document):
    name = db.StringField(required=True, max_length=100)
    description = db.StringField()
    status = db.StringField(default='running')
    priority = db.IntField(default=1, min_value=1, max_value=5)
    created_at = db.DateTimeField(default=db.func.now())

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at.isoformat()
        }
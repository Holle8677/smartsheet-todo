import datetime
import json

class Task():
    id: int
    title: str
    description: str
    due_date: str
    completed: bool

    def __init__(self, id = None, title = 'Task', description = 'A pressing task', due_date = datetime.date.today(), completed = False):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = completed

    def __iter__(self):
        yield from {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "completed": self.completed
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()


class TaskEncoder(json.JSONEncoder):
    def default(self, obj):
        return dict(obj)    
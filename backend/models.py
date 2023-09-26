import datetime
import json

class Task():
    id: int
    title: str
    description: str
    due_date: str
    completed: bool

    def __init__(self, id:int = None, title:str = 'Task', description:str = 'A pressing task', due_date:str = '', completed:bool = False):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = completed

    def _load_from_dict(self, data:dict):
        if 'id' in data:
            self.id = data.get('id')
        if 'title' in data:
            self.title = data.get('title')
        if 'description' in data:
            self.description = data.get('description')
        if 'due_date' in data:
            self.due_date = data.get('due_date')
        if 'completed' in data:
            self.completed = data.get('completed')

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
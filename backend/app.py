from datetime import datetime
import logging

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from json import dumps,loads
from marshmallow import ValidationError

import smartsheet_service
from schemas import TaskSchema
from models import Task, TaskEncoder

logging.basicConfig(filename=f'backend/logs/todo-smartsheet-{datetime.now().strftime("%Y-%m-%dT%H-%M-%S")}.log', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger('todo')

app = Flask(__name__)
cors = CORS(app)
logger.info('Todo app started')
smart_service = smartsheet_service.Smartsheet_service()

# @app.after_request
# def apply_caching(response):
#     response.headers["X-Frame-Options"] = "SAMEORIGIN"
#     return response

@app.get('/api/tasks/')
@cross_origin()
def get_tasks():
    tasks = smart_service.fetch_all_tasks()
    
    return dumps(tasks, cls = TaskEncoder)

@app.post('/api/tasks/')
@cross_origin()
def add_tasks():
    request_data = request.json
    schema = TaskSchema()
    try:
        results = schema.load(request_data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_task = Task()
    new_task._load_from_dict(request_data)
    smart_service.add_tasks([new_task])

    return jsonify('success')
    pass

@app.put('/api/tasks/<int:task_id>')
@cross_origin()
def update_tasks():
    pass

@app.delete('/api/tasks/<task_id>')
@cross_origin()
def delete_tasks(task_id):
    try:
        smart_service.delete_tasks([task_id])
        return jsonify('success')
    except Exception as e:
        return jsonify('failure')



# logging?
# where to hold cached sheet?
# error handling
# work directly with smartsheet data model? tracking row ids into the task model?
# pass smartsheet success or error on to user
from flask import Flask
from flask_cors import CORS, cross_origin
from json import dumps,loads
from models import TaskEncoder
from datetime import datetime
import logging

import smartsheet_service

logging.basicConfig(filename=f'backend/logs/todo-smartsheet-{datetime.now().strftime("%Y-%m-%dT%H-%M-%S")}.log', encoding='utf-8', level=logging.DEBUG)

app = Flask(__name__)
cors = CORS(app)
logging.info('Todo app started')
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

@app.post('/api/tasks/<int:task_id>')
@cross_origin()
def add_tasks():
    pass

@app.put('/api/tasks/<int:task_id>')
@cross_origin()
def update_tasks():
    pass

@app.delete('/api/tasks/<int:task_id>')
@cross_origin()
def delete_tasks():
    pass




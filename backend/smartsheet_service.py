from models import Task

import config
import time
import smartsheet
import logging
import os

logger = logging.getLogger('todo')

class Smartsheet_service():
    def __init__(self):
        self.task_sheet_id = os.getenv('TASK_SHEET_ID')
        self.smart = smartsheet.Smartsheet()
        logger.info('Initial Smartsheet connection opened')
        self.smart.errors_as_exceptions(True)
        self._fetch_sheet()
        

    def fetch_all_tasks(self):
        if not self.task_sheet or self.task_sheet_ttl < time.time():
            self._fetch_sheet()
        tasks = []
        for row in self.task_sheet.rows:
            tasks.append(self._task_from_row(row))
        return tasks

    def delete_tasks(self, task_ids: list[int]):
        self.smart.Sheets.delete_rows(self.task_sheet_id, task_ids)
        self._fetch_sheet()

    def update_tasks(self, tasks: list[Task]):
        updated_rows = []
        for task in tasks:
            updated_rows.append(self._row_from_task(task))
        self.smart.Sheets.update_rows(self.task_sheet_id, updated_rows)
        self._fetch_sheet()

    def add_tasks(self, tasks: list[Task]):
        new_rows = []
        for task in tasks:
            new_rows.append(self._row_from_task(task))
        self.smart.Sheets.add_rows(self.task_sheet_id, new_rows)
        self._fetch_sheet()

    def _fetch_sheet(self):
        self.task_sheet = self.smart.Sheets.get_sheet(self.task_sheet_id)
        logger.info('DB sheet re-fetched')
        self.task_sheet_ttl = time.time() + config.TTL
        self.column_map = {}

        for column_name in config.COLUMN_NAMES:
            for column in self.task_sheet.columns:
                if column_name == column.title:
                    self.column_map[column_name] = column.id
                    break
            else:
                pass # throw new specified sheet not compatible exception

    def _row_from_task(self, task: Task):
        title_cell = smartsheet.models.Cell()
        title_cell.column_id = self.column_map[config.TITLE_COLUMN_NAME]
        title_cell.value = task.title

        description_cell = smartsheet.models.Cell()
        description_cell.column_id = self.column_map[config.DESCRIPTION_COLUMN_NAME]
        description_cell.value = task.description

        due_date_cell = smartsheet.models.Cell()
        due_date_cell.column_id = self.column_map[config.DUE_DATE_COLUMN_NAME]
        due_date_cell.value = task.due_date

        completed_cell = smartsheet.models.Cell()
        completed_cell.column_id = self.column_map[config.COMPLETED_COLUMN_NAME]
        completed_cell.value = task.completed

        new_row = smartsheet.models.Row()
        new_row.cells.extend([title_cell, description_cell, due_date_cell, completed_cell])

        if task.id is not None:
            new_row.id = task.id
        
        return new_row

    def _task_from_row(self, row: smartsheet.models.Row):
        new_task = Task()
        for cell in row.cells:
            if cell.column_id == self.column_map[config.TITLE_COLUMN_NAME]:
                new_task.title = cell.value
            elif cell.column_id == self.column_map[config.DESCRIPTION_COLUMN_NAME]:
                new_task.description = cell.value
            elif cell.column_id == self.column_map[config.DUE_DATE_COLUMN_NAME]:
                new_task.due_date = cell.value
            elif cell.column_id == self.column_map[config.COMPLETED_COLUMN_NAME]:
                new_task.completed = cell.value

        new_task.id = row.id
        return new_task


    
        


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Task Manager")

class Task(BaseModel):
    id: int
    title: str
    description: str = ""
    completed: bool = False

# In-memory store for demo purposes
_tasks: List[Task] = []

@app.get("/tasks", response_model=List[Task])
def read_tasks():
    return _tasks

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    _tasks.append(task)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: Task):
    for idx, t in enumerate(_tasks):
        if t.id == task_id:
            _tasks[idx] = task
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for idx, t in enumerate(_tasks):
        if t.id == task_id:
            _tasks.pop(idx)
            return
    raise HTTPException(status_code=404, detail="Task not found")


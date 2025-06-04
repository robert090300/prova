import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from fastapi.testclient import TestClient
from src.app import app, Task

client = TestClient(app)

def test_create_read_update_delete_task():
    # Create a task
    response = client.post("/tasks", json={"id": 1, "title": "Test task"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test task"

    # Read tasks
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert any(task["id"] == 1 for task in data)

    # Update task
    response = client.put("/tasks/1", json={"id": 1, "title": "Updated task", "completed": True})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated task"
    assert data["completed"]

    # Delete task
    response = client.delete("/tasks/1")
    assert response.status_code == 204

    # Ensure task is gone
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert not any(task["id"] == 1 for task in data)

import os, sys
from fastapi import FastAPI

# Add the parent directory to the path so we can import the tasking_request module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sensor_tasking.tasking_request import TaskingRequest


# create a FastAPI instance
app = FastAPI()

# create a list to store the tasking requests
tasking_requests = []

# function to handle PUT requests containing TaskingRequest objects
@app.put("/tasking_requests/")
async def create_tasking_request(tasking_request: TaskingRequest):
    tasking_requests.append(tasking_request)
    return {"message": "Tasking request added to queue."}

# function to handle GET requests for the tasking queue
@app.get("/tasking_requests/")
async def get_tasking_requests():
    return tasking_requests

# function to handle GET requests for a specific tasking request
@app.get("/tasking_requests/{task_id}")
async def get_tasking_request(task_id: int):
    for tasking_request in tasking_requests:
        if tasking_request.task_id == task_id:
            return tasking_request
    return {"message": "Tasking request not found."}

# function to handle DELETE requests for a specific tasking request
@app.delete("/tasking_requests/{task_id}")
async def delete_tasking_request(task_id: int):
    for tasking_request in tasking_requests:
        if tasking_request.task_id == task_id:
            tasking_requests.remove(tasking_request)
            return {"message": "Tasking request deleted."}
    return {"message": "Tasking request not found."}


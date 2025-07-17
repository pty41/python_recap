from fastapi import FastAPI, HTTPException
from config import Settings
from schemas import InstanceCreate, Instance, InstanceStatus, StopResponse
from typing import List
from exceptions import InvalidInstanceIDException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from storage import create_instance, read_instance, delete_instance, list_instances

settings = Settings()
mock_db = {
    1: {"name": "api-server", "region": "us-west-1"},
    2: {"name": "db-server", "region": "ap-southeast-1"}
}
app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

@app.get("/")
def read_root():
    return {"message": "Hello ~ ~"}

@app.get("/hello/{name}")
def say_hello(name: str, title: str="Engineer"):
    return {"message": f"Hello {name} {title}"}

@app.get("/greet")
def say_hello_lan(name: str="Shan", language: str="en"):
    greetings = {
        "en": "Hello",
        "zh": "你好",
        "fr": "Bonjour"
    }
    greet_word = greetings.get(language, "not match language")
    return {"greeting": f"{greet_word}, {name}!"}

@app.get("/square/{number}")
def square(number: int):
    return {"number": number, "square": number*number}

@app.get("/status")
def status():
    return {"status": "ok", "version": settings.VERSION}


@app.post("/instances")
def mock_create_instance(instance:InstanceCreate):
    return {
        "message": "Instance created successfully!",
        "data": instance.dict()
        }

#########Customize Exception + Handler##########

@app.exception_handler(InvalidInstanceIDException)
async def invalid_instance_handler(request: Request, exc: InvalidInstanceIDException):
    return JSONResponse(
        status_code=422,
        content={
            "error": "InvalidInstanceID",
            "message": f"Instance ID {exc.instance_id} is invalid (must be positive integer)"
        }
    )

@app.get("/instances/{instance_id}")
def get_instance(instance_id: int):
    if instance_id < 0:
        raise InvalidInstanceIDException(instance_id)

    if instance_id not in mock_db:
        raise HTTPException(status_code=404, detail="Instance not found")

    return mock_db[instance_id]


################## Async CRUD #################


app.post("/instances_async", response_model=Instance)
async def create(data: Instance):
    return await create_instance(data)


@app.get("/instances_async/{instance_id}", response_model=Instance)
async def read(instance_id: str):
    instance = await read_instance(instance_id)
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    return instance


@app.get("/instances_async", response_model=List[Instance])
async def list_all():
    return await list_instances()

@app.delete("/instances_async/{instance_id}")
async def delete(instance_id: str):
    success = await delete_instance(instance_id)
    if not success:
        raise HTTPException(status_code=404, detail="Instance not found")
    return {"message": "Deleted successfully"}

@app.patch("/instances/{instance_id}/stop", response_model=StopResponse)
async def instance_stop(instance_id: str):
    instance = await read_instance(instance_id)
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    instance.status = InstanceStatus.STOPPED
    return {"message": f"Instance {instance_id} stopped", "status": str(instance.status)}

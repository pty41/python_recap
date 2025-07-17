from fastapi import Request
from fastapi.responses import JSONResponse

class InvalidInstanceIDException(Exception):
    def __init__(self, instance_id: int):
        self.instance_id = instance_id
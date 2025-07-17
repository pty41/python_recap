from pydantic import BaseModel, Field, validator, constr, conint
from typing import List, Optional
from enum import Enum

class InstanceStatus(str, Enum):
    RUNNING = "running"
    STOPPED = "stopped"

class Owner(BaseModel): #Nested Strucuture
    id: int
    name: str

class Region(str, Enum): #Strengthen field constraints use Enum
    US_WEST = "us-west-1"
    US_EAST = "us-east-1"
    AP_SE = "ap-southeast-1"

class InstanceCreate(BaseModel):
    name: constr(min_length=3, max_length=20, regex=r"^[a-z0-9-]+$") = Field(..., example="dev-instance")
    region: Region = Field(..., example="us-west-1")
    cpu: conint(ge=1, le=64) = Field(..., description="CPU cores, 1-64 only")
    memory: Optional[int] = Field(8, example=16)
    tags: Optional[List[str]] = Field(default_factory=list)
    owner: Owner
    status: InstanceStatus = InstanceStatus.RUNNING

    @validator("memory") #Strengthen field constraints use validator
    def memory_must_be_power_of_two(cls, v):
        if v & (v - 1) != 0:
            raise ValueError("memory must be power of 2")
        return v


class Instance(BaseModel):
    id: str #UUID
    name: str
    region:Region
    cpu: int
    memory: Optional[int] = Field(8, example=16)
    tags: Optional[List[str]] = Field(default_factory=list)
    owner: Owner
    status: InstanceStatus = InstanceStatus.RUNNING

class StopResponse(BaseModel):
    message: str
    status: str
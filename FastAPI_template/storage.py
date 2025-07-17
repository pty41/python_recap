from typing import Dict, Optional, List
from schemas import Instance, InstanceStatus
import uuid

instance_db: Dict[str, Instance] = {} #local database

async def create_instance(data: Instance) -> Instance:
    new_id = str(uuid.uuid4())
    instance = Instance(id=new_id, status=InstanceStatus.RUNNING, **data.dict())
    instance_db[new_id] = instance
    return instance

async def read_instance(instance_id: str) -> Optional[Instance]:
    return instance_db.get(instance_id, None)

async def delete_instance(instance_id: str) -> bool:
    return instance_db.pop(instance_id, None) is not None


async def list_instances() -> List[Instance]:
    return list(instance_db.values())
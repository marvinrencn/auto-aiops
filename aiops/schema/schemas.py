from pydantic import BaseModel
from typing import List
from datetime import datetime
from pydantic import BaseModel

class Learnware(BaseModel):
    id: int
    name: str
    description: str = None

    class Config:
        orm_mode = True

class BaseRequest(BaseModel):
    pass


class MachineAnomalyDetectionRequest(BaseRequest):
    index_name: str
    resource_name: str
    values: List


class BaseResponse(BaseModel):
    res: bool = True
    message: str = ""


class MachineAnomalyDetectionResponse(BaseResponse):
    data: List[int] = []

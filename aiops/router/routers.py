from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from aiops.database import repository, models
from aiops.database.database import SessionLocal, engine
from aiops.learnware.MachineLearnware import MachineLearnware
from aiops.schema import schemas


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


router = APIRouter()


@router.get("/learnware/", response_model=List[schemas.Learnware])
async def get_all_learnwares(db: Session = Depends(get_db)):
    learnwares = repository.get_learnwares(db)
    return learnwares


@router.post("/anomaly/{learnware_name}", response_model=schemas.MachineAnomalyDetectionResponse)
async def anomaly_machine(learnware_name, request: schemas.MachineAnomalyDetectionRequest):
    #TODO: 目前只支持一个学件，之后需要增加支持数量，并根据学件名称实现学件选择
    learnware = MachineLearnware()

    values = learnware.preprocess_data(request.values)
    predict = learnware.call(request.index_name, request.resource_name, values)

    result = schemas.MachineAnomalyDetectionResponse()
    result.res = True
    result.message = "anomacly detection succuss"
    result.data = list(predict)

    return result

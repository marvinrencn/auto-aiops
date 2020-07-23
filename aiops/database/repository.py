import datetime
from sqlalchemy.orm import Session
from aiops.database import models


# Learnware


def get_learnwares(db: Session):
    return db.query(models.Learnware).all()


def get_learnware_by_id(db: Session, learnware_id):
    return db.query(models.LearnwareModel).get(learnware_id)


def get_learnware_by_name(db: Session, learnware_name):
    return db.query(models.Learnware).filter(models.Learnware.name == learnware_name).first()


# Datasource


def get_datasource_by_id(db: Session, datasource_id):
    return db.query(models.Datasource).get(datasource_id)


# LearnwareModel


def get_learnware_model(db: Session, learnware_id, model_name):
    return db.query(models.LearnwareModel)\
        .filter(models.LearnwareModel.learnware_id == learnware_id, models.LearnwareModel.name == model_name)\
        .all()


def find_learnware_model_by_index_name(db: Session, learnware_id, index_name):
    return db.query(models.LearnwareModel)\
        .filter(models.LearnwareModel.learnware_id == learnware_id, models.LearnwareModel.index_name == index_name)\
        .all()


def insert_learnware_model(db: Session, model: models.LearnwareModel):
    model.updated_by = datetime.datetime.now()
    model.created_by = datetime.datetime.now()
    model.version = 1
    db.add(model)
    db.commit()


def update_learnware_model(db: Session, model: models.LearnwareModel):
    model.updated_by = datetime.datetime.now()
    model.version = model.version + 1
    db.commit()


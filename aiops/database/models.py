from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from aiops.database.database import Base

class Datasource(Base):
    __tablename__="datasource"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))
    driver = Column(String(255))
    host = Column(String(255))
    port = Column(Integer)
    username = Column(String(255))
    password = Column(String(255))
    database = Column(String(64))

    learnwares = relationship("Learnware")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Learnware(Base):
    __tablename__ = "learnware"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), unique=True, index=True)
    description = Column(String(1024))
    datasource_id = Column(Integer, ForeignKey('datasource.id'))
    train_data_fetch_sql = Column(String(2048))
    train_data_max_size = Column(Integer, default=100000)
    model_select_policy = Column(String(64), default="one-to-one")
    models = relationship("LearnwareModel")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class LearnwareModel(Base):
    __tablename__ = "learnware_model"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(1024))
    learnware_id = Column(Integer)
    resource_name = Column(String(255))
    index_name = Column(String(255))
    file_path = Column(String(1024))
    created_by = Column(DateTime)
    updated_by = Column(DateTime)
    version = Column(Integer, default=0)

    learnware_id = Column(Integer, ForeignKey('learnware.id'))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}





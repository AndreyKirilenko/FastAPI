from datetime import datetime
from sqlalchemy import Column, Integer, Text, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


class Warehouse(Base):
    id = Column(Integer, primary_key=True, index=True)
    warehouseID = Column(Integer, )
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    workTime = Column(String, nullable=False)
    acceptsQR =  Column(Boolean, )


class Coefficient(Base):
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, )
    now_datetime = Column(DateTime, default=datetime.now)
    coefficient = Column(Integer, )
    warehouseID = Column(Integer, )
    warehouseName = Column(String, nullable=False)
    boxTypeName =  Column(String, nullable=False)
    boxTypeID = Column(Integer, nullable=True)

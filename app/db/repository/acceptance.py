from sqlalchemy.orm import Session
import datetime

from schemas.acceptance import CreateWarehouse, CreateCoefficient
from db.models.acceptance import Warehouse, Coefficient
# from core.hashing import Hasher


def create_new_warehouse(warehouse:CreateWarehouse,db:Session):
    
    warehouse = Warehouse(
        warehouseID = warehouse.warehouseID,
        name = warehouse.name,
        address = warehouse.address,
        workTime = warehouse.workTime,
        acceptsQR = warehouse.acceptsQR,
    )
    db.add(warehouse)
    db.commit()
    db.refresh(warehouse)
    return warehouse

def create_new_coefficient(coefficient:CreateCoefficient,db:Session):
    # print(type(coefficient))
    # import ipdb; ipdb.set_trace()
    coefficient = Coefficient(
        # id = coefficient.id,
        date = coefficient.date,
        coefficient = coefficient.coefficient,
        warehouseID = coefficient.warehouseID,
        warehouseName = coefficient.warehouseName,
        boxTypeName = coefficient.boxTypeName,
        boxTypeID = coefficient.boxTypeID,
        )
    db.add(coefficient) 
    db.commit()
    db.refresh(coefficient)
    return coefficient 

from pydantic import BaseModel,EmailStr, Field



class CreateWarehouse(BaseModel):
    warehouseID: int
    name: str
    address: str
    workTime: str
    acceptsQR: bool


class CreateCoefficient(BaseModel):
    # id: float
    date: str # ???
    coefficient: float
    warehouseID: float
    warehouseName: str
    boxTypeName: str
    boxTypeID: float
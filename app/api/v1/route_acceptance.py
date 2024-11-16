from fastapi import APIRouter, status
from sqlalchemy.orm import Session
from fastapi import Depends
import logging
from fastapi.responses import JSONResponse

from schemas.acceptance import CreateCoefficient, CreateWarehouse
from db.session import get_db
from db.repository.acceptance import create_new_coefficient, create_new_warehouse
import requests
from settings import settings
from db.models.acceptance import Warehouse, Coefficient
from sqlalchemy import desc

router = APIRouter()


# @router.post("/warehouse",response_model=CreateWarehouse, status_code=status.HTTP_201_CREATED)
# def create_warehouse(warehouse : CreateWarehouse, db: Session = Depends(SessionLocal)):
#     warehouse = create_new_warehouse(warehouse=warehouse,db=db)
#     return warehouse 

@router.post("/warehouse",response_model=CreateWarehouse, status_code=status.HTTP_201_CREATED)
def create_warehouse(warehouse : CreateWarehouse, db: Session = Depends(get_db)):
    warehouse = create_new_warehouse(warehouse=warehouse,db=db)
    return warehouse 

@router.post("/coefficient",response_model=CreateCoefficient, status_code=status.HTTP_201_CREATED)
def create_coefficient(coefficient : CreateCoefficient, db: Session = Depends(get_db)):
    coefficient = create_new_coefficient(coefficient=coefficient, db=db)
    return coefficient 

# # @router.post("/coefficient",response_model=CreateCoefficient, status_code=status.HTTP_201_CREATED)
# def set_coefficient(coefficient : CreateCoefficient, db: Session = Depends(get_db)):
#     coefficient = create_new_coefficient(coefficient=coefficient, db=db)
#     return coefficient 


@router.get('/get_warehouse_coefficient/{warehouseID}')
def get_warehouse_coefficient(warehouseID, db: Session = Depends(get_db)):
    """"Запрашивает коэффициенты складов проверяет изменился ли коэффициент
    если изменился создает объект с новым коэфф"""
    headers = {
        'Authorization': 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQwOTA0djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTc0MjQwMzM1MiwiaWQiOiIwMTkyMDM3Yy1hMDY2LTc5NTMtYTcyYi04MzUwMTBmNmY5NjYiLCJpaWQiOjQ4NzQ3NTMwLCJvaWQiOjEwNjcwNjUsInMiOjEwNzM3NTAwMTQsInNpZCI6Ijc1OTRlMTllLWEzNTYtNDRiMy05YWVjLWE0N2ZlZmQ3MmYyNCIsInQiOmZhbHNlLCJ1aWQiOjQ4NzQ3NTMwfQ.3M-wVY7O8jv6xE_Xq21ZVdhYSmaGAXeBm_1Q_JuVc3vcFWBuqTpZVBMXalH0YMV7Pvv-ZnrY1ourgW9bEKSHqA',
        'Content-Type': 'application/json'
    }
    url = f"https://supplies-api.wildberries.ru/api/v1/acceptance/coefficients?warehouseIDs={warehouseID}"
    try:
        response = requests.get(url,  headers=headers)
        if response.json() is None:
            logging.error(F"Ответ от API WB пустой. Возможно запрошен неверный ID склада. {response.status_code}")
            return JSONResponse(content={"message": "Ошибка получения данных WB API"}, status_code=404)
    except requests.exceptions.ConnectionError as err:
        logging.error(F"Ошибка подключения ⛔. {err}")
        return JSONResponse(content={"message": "Ошибка подключения к WB API"}, status_code=response.status_code)
    # import ipdb; ipdb.set_trace()
    for res in response.json():
        try:
            boxTypeID = res["boxTypeID"]
        except:
            boxTypeID = 0
        
        if boxTypeID != 2: # Если это не короб, переходим к следующей итерации
            print("Пропуск. не короб")
            continue
        # Ищем такой же объект и проверяем коэффициент с последней датой,
        # Если коэфф тот же, то пропускаем идем дальше
        # Если коэфф другой, сохраняем с новой датой
        warehouse = db.query(Coefficient).filter(
            (Coefficient.warehouseID == res["warehouseID"]) &
            (Coefficient.date == res["date"])
            ).order_by(desc(Coefficient.now_datetime)).first()
        
        if warehouse: # Проверяем совпадает ли коэфф, если да, то пропускаем, переходим к следующей итерации
            if warehouse.coefficient == res["coefficient"]:
                print("Пропуск. совп коэфф")
                continue
        # import ipdb; ipdb.set_trace()
        # Сюда доходим если склада еще нет или поменялся
        try:
            crt_cff = CreateCoefficient(
                warehouseID=res["warehouseID"],
                warehouseName=res["warehouseName"],
                coefficient=res["coefficient"],
                date=res["date"],
                boxTypeName=res["boxTypeName"],
                boxTypeID=boxTypeID
                )
        except Exception as err:
            logging.error(F"Ошибка получения данных ⛔. {err}")
            return JSONResponse(content={"message": "Ошибка получения данных"}, status_code=response.status_code)
    
        create_new_coefficient(crt_cff, db=db)
        print("----  Добавили объект")
    return JSONResponse(content={"message": "Все ОК"}, status_code=response.status_code)
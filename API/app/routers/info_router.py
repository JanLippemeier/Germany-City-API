from fastapi import Depends, APIRouter
from sqlalchemy import func, cast, String, Integer
from sqlalchemy.orm import Session
from db import database, models


router = APIRouter()



@router.get("/states")
def states(db:Session=Depends(database.get_db)):
    return db.query(models.city).with_entities(
        models.state.name,
        func.count(models.city.id).label("city_count"),
        func.sum(models.city.population).label("population"),
        func.sum(models.city.female_population).label("female_population"),
        func.floor(func.sum(models.city.area)).label("area")
    ).join(models.city.state
    ).group_by(models.state.name
    ).order_by(
        models.state.name
    ).all()

@router.get("/cities")
def cities(
        db:Session=Depends(database.get_db),
        city_name:str="",
        state_name:str="",
        postal_code:int=None,
        latitude:float=None,
        longitude:float=None
    ):
    query = db.query(models.city).with_entities(
        models.city.id,
        models.city.name,
        models.city.postal_code,
        models.state.name.label("state_name"),
        models.city.population,
        models.city.female_population,
        models.city.area,
        models.city.latitude,
        models.city.longitude,
    ).join(models.city.state)
    if len(city_name.strip()) > 0:
        query = query.filter(models.city.name.ilike("%"+city_name+"%"))
    if len(state_name.strip()) > 0:
        query = query.filter(func.lower(models.state.name)==state_name.lower())        
    if postal_code is not None:
        query = query.filter(cast(models.city.postal_code, String).like(str(postal_code)+"%"))
    if latitude is not None and longitude is not None:
        print("Hello")
        query = query.order_by((func.pow(models.city.latitude-latitude,2) + func.pow(models.city.longitude-longitude,2))).limit(10)
    return query.all()
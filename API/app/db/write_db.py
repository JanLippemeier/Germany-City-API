from io import BytesIO
import openpyxl
import pandas as pd
from sqlalchemy.orm import Session
from db import models

def write_import_db(excelFile:BytesIO, db:Session):

    wb = openpyxl.load_workbook(excelFile)

    ws = wb.active

    excel_columns = ["c1","c2","state_id","c3","c4","c5","c6",
    "city_name","area","population","c7","female_population",
    "c8","postal_code","longitude","latitude","c9","c10","c11","c12"]

    columns = ["state_id","city_name","area","population",
    "female_population","postal_code","longitude","latitude"]

    df = pd.DataFrame(data=ws.iter_rows(values_only=True),columns=excel_columns)

    df = df.loc[df["state_id"].notnull()]

    states = df.loc[(df["c1"].notnull())&(~df["c2"].notnull())&(~df["c3"].notnull())&(~df["c4"].notnull())]
    existing_states = list(map((lambda x:x.name),db.query(models.state).all()))
    new_states = [models.state(id=state.state_id, name=state.city_name) for state in states[["city_name","state_id"]].itertuples() if state.city_name not in existing_states]
    db.add_all(new_states)
    states = db.query(models.state).all()

    df =  df.loc[pd.to_numeric(df['postal_code'], errors='coerce').notnull()]
    df = df.reset_index()
    df = df[columns]
    df["city_name"] = df["city_name"].str.replace(", Stadt","").str.replace(", Hansestadt","").str.replace(", Landeshauptstadt","")
    df["longitude"] = df["longitude"].str.replace(",",".")
    df["latitude"] = df["latitude"].str.replace(",",".")


    db.query(models.city).delete()
    new_cities = [
        models.city(
            id=city.Index+1,
            name=city.city_name,
            state_id=city.state_id,
            area=city.area,
            population=city.population,
            female_population=city.female_population,
            postal_code=city.postal_code,
            longitude=city.longitude,
            latitude=city.latitude
        ) for city in df.itertuples()]

    db.add_all(new_cities)
    db.commit()
import requests
from fastapi import Depends, APIRouter, Response
from io import BytesIO
from sqlalchemy.orm import Session
from db import database, write_db
from pydantic_models import api_key_body
import os

router = APIRouter()
url = 'https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/Archiv/GVAuszugQ/AuszugGV3QAktuell.xlsx?__blob=publicationFile'

@router.post("/")
def update(key_body:api_key_body,db:Session=Depends(database.get_db)):
    if key_body.key == os.environ.get("DEV_API_KEY"):
        r = requests.get(url, allow_redirects=True)
        file = BytesIO(r.content)
        write_db.write_import_db(file, db)
        return "Updated"
    else:
        return Response('{"message":"Unauthorized","code":403}', 403)

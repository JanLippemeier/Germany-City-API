from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PW = os.environ.get("DEV_DB_PW")
print(DB_PW)
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{DB_PW}@{DB_HOST}/Germany"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
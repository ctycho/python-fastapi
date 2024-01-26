from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# import psycopg2
# from psycopg2.extras import RealDictCursor
DB_URL: list = [
    'postgresql://', settings.db_username,
    ':', settings.db_password,
    '@', settings.db_hostname,
    ':', settings.db_port,
    '/', settings.db_name
]

SQLALCHEMY_DATABASE_URL = "".join(DB_URL)
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         # if password wrong still acceptes
#         conn = psycopg2.connect(host='localhost',
#                                 database='fastapi',
#                                 user='ilnurgumerov',
#                                 password='qwerty',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Connection succesfull')
#         break
#     except Exception as ex:
#         print('Connection failed', ex)
#         time.sleep(5)

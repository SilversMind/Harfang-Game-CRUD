from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.core.models import Base
from src.constants import (
    MYSQL_DATABASE,
    MYSQL_PASSWORD,
    MYSQL_USER,
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_ROOT_PASSWORD,
)

# Create the initial engine and connection to create the database
initial_engine = create_engine(
    f"mysql+mysqlconnector://root:{MYSQL_ROOT_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}"
)
connection = initial_engine.connect()

connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}"))
connection.execute(
    text(f"GRANT ALL PRIVILEGES ON {MYSQL_DATABASE}.* TO '{MYSQL_USER}'@'%';")
)

connection.close()

DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

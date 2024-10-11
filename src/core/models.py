from sqlalchemy import Column, Integer, String, Date, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    release_date = Column(Date, nullable=False)
    studio = Column(String(255), nullable=False)
    ratings = Column(Integer, nullable=False)
    platforms = Column(JSON, nullable=False)

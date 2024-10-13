from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

game_platforms = Table(
    'game_platforms',
    Base.metadata,
    Column('game_id', Integer, ForeignKey('games.id')),
    Column('platform_id', Integer, ForeignKey('platforms.id'))
)

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    release_date = Column(Date, nullable=False)
    studio = Column(String(255), nullable=False)
    ratings = Column(Integer, nullable=False)

    platforms = relationship("Platform", secondary="game_platforms", back_populates="games")

class Platform(Base):
    __tablename__ = 'platforms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)

    games = relationship("Game", secondary="game_platforms", back_populates="platforms")
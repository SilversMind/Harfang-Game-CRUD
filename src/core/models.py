from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Foo(Base):
    __tablename__ = 'foo'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    
    bar = relationship("Bar", back_populates="foo")

class Bar(Base):
    __tablename__ = 'bar'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    foo_id = Column(Integer, ForeignKey('foo.id'))

    foo = relationship("Foo", back_populates="bar")
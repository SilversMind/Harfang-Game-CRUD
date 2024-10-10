from fastapi import APIRouter, Depends
from src.core.dependencies import get_db
from src.core.models import Foo

router = APIRouter()

@router.get("/")
def ping(db=Depends(get_db)):
    db.add(Foo(name="foo1"))
    db.commit()
    res = db.query(Foo).filter(Foo.id == 1).first()
    return {"ping": res.name}
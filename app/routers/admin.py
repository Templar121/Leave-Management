from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import database, crud
from ..auth import get_current_hr

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/db-dump")
def get_full_database(db: Session = Depends(database.get_db), hr=Depends(get_current_hr)):
    """
    HR-only endpoint: returns full database snapshot 
    (all employees + their leaves).
    """
    return crud.get_all_employees_with_leaves(db)

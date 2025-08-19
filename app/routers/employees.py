from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database
from ..auth import get_current_hr


router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/all", response_model=list[schemas.EmployeeResponse])
def list_employees(db: Session = Depends(database.get_db), hr=Depends(get_current_hr)):
    return crud.get_all_employees(db)

@router.post("/", response_model=schemas.EmployeeResponse)
def create_employee(emp: schemas.EmployeeCreate, db: Session = Depends(database.get_db), hr=Depends(get_current_hr)):
    return crud.create_employee(db, emp)

@router.get("/{emp_id}", response_model=schemas.EmployeeResponse)
def get_employee(emp_id: int, db: Session = Depends(database.get_db), hr=Depends(get_current_hr)):
    emp = crud.get_employee(db, emp_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database, models

router = APIRouter(prefix="/leaves", tags=["Leaves"])

@router.post("/{emp_id}", response_model=schemas.LeaveResponse)
def apply_leave(emp_id: int, leave: schemas.LeaveCreate, db: Session = Depends(database.get_db)):
    emp = crud.get_employee(db, emp_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    if leave.start_date < emp.joining_date:
        raise HTTPException(status_code=400, detail="Leave before joining date not allowed")

    if leave.end_date < leave.start_date:
        raise HTTPException(status_code=400, detail="End date before start date")

    days_requested = (leave.end_date - leave.start_date).days + 1
    if days_requested > emp.leave_balance:
        raise HTTPException(status_code=400, detail="Insufficient leave balance")

    return crud.apply_leave(db, emp_id, leave)

@router.put("/{leave_id}/status")
def update_status(leave_id: int, status: schemas.LeaveStatus, db: Session = Depends(database.get_db)):
    leave = crud.update_leave_status(db, leave_id, status)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    return leave

@router.get("/balance/{emp_id}")
def leave_balance(emp_id: int, db: Session = Depends(database.get_db)):
    balance = crud.get_leave_balance(db, emp_id)
    if balance is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"employee_id": emp_id, "leave_balance": balance}

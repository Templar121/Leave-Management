from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database, models
from ..auth import get_current_hr
from ..models import HRUser

router = APIRouter(prefix="/leaves", tags=["Leaves"])

@router.post("/{emp_id}", response_model=schemas.LeaveResponse)
def apply_leave(emp_id: int, leave: schemas.LeaveCreate, db: Session = Depends(database.get_db)):
    emp = crud.get_employee(db, emp_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    # 🚫 Leave before joining
    if leave.start_date < emp.joining_date:
        raise HTTPException(status_code=400, detail="Leave before joining date not allowed")

    # 🚫 End date before start date
    if leave.end_date < leave.start_date:
        raise HTTPException(status_code=400, detail="End date cannot be before start date")

    # 🚫 Zero/negative duration
    days_requested = (leave.end_date - leave.start_date).days + 1
    if days_requested <= 0:
        raise HTTPException(status_code=400, detail="Invalid leave duration")

    # 🚫 Insufficient balance
    if days_requested > emp.leave_balance:
        raise HTTPException(status_code=400, detail="Insufficient leave balance")

    # 🚫 Overlapping requests (check existing leaves)
    overlapping = db.query(models.Leave).filter(
        models.Leave.employee_id == emp_id,
        models.Leave.status.in_([models.LeaveStatus.PENDING, models.LeaveStatus.APPROVED]),
        models.Leave.start_date <= leave.end_date,
        models.Leave.end_date >= leave.start_date
    ).first()
    if overlapping:
        raise HTTPException(status_code=400, detail="Leave overlaps with existing request")

    return crud.apply_leave(db, emp_id, leave)


@router.put("/{leave_id}/status")
def update_status(
    leave_id: int,
    status: schemas.LeaveStatus,
    db: Session = Depends(database.get_db),
    hr=Depends(get_current_hr)   # ✅ HR-only
):
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

@router.delete("/{leave_id}/withdraw")
def withdraw_leave(leave_id: int, db: Session = Depends(database.get_db)):
    result = crud.withdraw_leave(db, leave_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Leave not found")
    if result == "not_pending":
        raise HTTPException(status_code=400, detail="Only pending leaves can be withdrawn")
    return {"message": "Leave application withdrawn successfully"}
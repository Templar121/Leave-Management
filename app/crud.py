from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date

def create_employee(db: Session, emp: schemas.EmployeeCreate):
    # 🚫 Duplicate Email Check
    existing = db.query(models.Employee).filter(models.Employee.email == emp.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    # 🚫 Invalid Joining Date (e.g. future date)
    if emp.joining_date > date.today():
        raise HTTPException(status_code=400, detail="Joining date cannot be in the future")

    new_emp = models.Employee(**emp.dict())
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return new_emp

def get_employee(db: Session, emp_id: int):
    return db.query(models.Employee).filter(models.Employee.id == emp_id).first()

def apply_leave(db: Session, emp_id: int, leave: schemas.LeaveCreate):
    employee = get_employee(db, emp_id)
    if not employee:
        return None

    new_leave = models.Leave(employee_id=emp_id, **leave.dict())
    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)
    return new_leave

def update_leave_status(db: Session, leave_id: int, status: str):
    leave = db.query(models.Leave).filter(models.Leave.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    # 🚫 Double approval prevention
    if leave.status == models.LeaveStatus.APPROVED and status == models.LeaveStatus.APPROVED:
        raise HTTPException(status_code=400, detail="Leave already approved")

    # 🚫 Expired leave cannot be approved
    from datetime import date
    if status == models.LeaveStatus.APPROVED and leave.end_date < date.today():
        raise HTTPException(status_code=400, detail="Cannot approve expired leave")

    leave.status = status

    if status == models.LeaveStatus.APPROVED:
        emp = leave.employee
        days = (leave.end_date - leave.start_date).days + 1
        if emp.leave_balance < days:
            raise HTTPException(status_code=400, detail="Insufficient balance at approval")
        emp.leave_balance -= days

    db.commit()
    db.refresh(leave)
    return leave

def get_leave_balance(db: Session, emp_id: int):
    emp = get_employee(db, emp_id)
    return emp.leave_balance if emp else None

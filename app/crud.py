from sqlalchemy.orm import Session
from . import models, schemas

def create_employee(db: Session, emp: schemas.EmployeeCreate):
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
    if leave:
        leave.status = status
        if status == models.LeaveStatus.APPROVED:
            emp = leave.employee
            days = (leave.end_date - leave.start_date).days + 1
            emp.leave_balance -= days
        db.commit()
        db.refresh(leave)
    return leave

def get_leave_balance(db: Session, emp_id: int):
    emp = get_employee(db, emp_id)
    return emp.leave_balance if emp else None

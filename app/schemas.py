from pydantic import BaseModel, EmailStr, constr
from datetime import date
from enum import Enum

class LeaveStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class EmployeeCreate(BaseModel):
    name: constr(min_length=1)
    email: EmailStr
    department: constr(min_length=1)
    joining_date: date

class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: str
    joining_date: date
    leave_balance: int

    class Config:
        orm_mode = True

class LeaveCreate(BaseModel):
    start_date: date
    end_date: date

class LeaveResponse(BaseModel):
    id: int
    start_date: date
    end_date: date
    status: LeaveStatus
    employee_id: int

    class Config:
        orm_mode = True

class HRUserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
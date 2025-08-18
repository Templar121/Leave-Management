from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum

class LeaveStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    department = Column(String, nullable=False)
    joining_date = Column(Date, nullable=False)
    leave_balance = Column(Integer, default=20)   # 20 leaves per year

    leaves = relationship("Leave", back_populates="employee")

class Leave(Base):
    __tablename__ = "leaves"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(Enum(LeaveStatus), default=LeaveStatus.PENDING)

    employee = relationship("Employee", back_populates="leaves")

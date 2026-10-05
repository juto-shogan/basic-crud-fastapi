from datetime import date
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from aw_api.models.base import Base


class Employee(Base):
    __tablename__ = "employee"
    __table_args__ = {"schema": "humanresources"}

    businessentityid: Mapped[int] = mapped_column(primary_key=True)
    jobtitle: Mapped[str] = mapped_column(String(50))
    gender: Mapped[str] = mapped_column(String(1))
    hiredate: Mapped[date]
    
    

class Department(Base):
    __tablename__ = "department"
    __table_args__ = {"schema": "humanresources"}
    
    departmentid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    
    
class EmployeeDepartmentHistory(Base):
    __tablename__ = "employeedepartmenthistory"
    __table_args__ = {"schema": "humanresources"}
    
    businessentityid: Mapped[int] = mapped_column(primary_key=True)
    departmentid: Mapped[int] = mapped_column(primary_key=True)
    startdate: Mapped[date] = mapped_column(primary_key=True)
    enddate: Mapped[date | None]
    
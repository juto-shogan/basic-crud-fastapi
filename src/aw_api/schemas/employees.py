from datetime import date
from pydantic import BaseModel

class Employee(BaseModel):
    businessentityid: int
    jobtitle: str
    gender: str
    hiredate: date


class DepartmentEmployee(BaseModel):
    name: str
    jobtitle: str
    hiredate: date

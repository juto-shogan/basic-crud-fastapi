from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date
from pydantic import BaseModel

from aw_api.database import get_db

router = APIRouter()


class Employee(BaseModel):
    businessentityid: int
    jobtitle: str
    gender: str
    hiredate: date


class DepartmentEmployee(BaseModel):
    name: str
    jobtitle: str
    hiredate: date


@router.get("/employee/{id}", response_model=Employee)
def get_employees(id: int, db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT * FROM humanresources.employee WHERE businessentityid = :employee_id"),
        {"employee_id": id}
    )
    info = result.mappings().first()
    if info is None:
        raise HTTPException(status_code=404, detail="ID doesn't exist, please check the ID")
    return info


@router.get("/departments/{id}/employees", response_model=list[DepartmentEmployee])
def get_current_employees(id: int, db: Session = Depends(get_db)):
    result = db.execute(
        text(
            """
            SELECT d.name, e.jobtitle, e.hiredate
            FROM humanresources.department AS d
            JOIN humanresources.employeedepartmenthistory
                USING(departmentid)
            JOIN humanresources.employee AS e
                USING(businessentityid)
            WHERE ENDDATE IS null AND departmentid = :departmentid
            """
        ),
        {"departmentid": id}
    )
    return result.mappings().all()
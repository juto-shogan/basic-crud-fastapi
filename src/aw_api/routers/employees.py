from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import text

from aw_api.database import get_db
from aw_api.schemas.employees import Employee, DepartmentEmployee
from aw_api.repositories import employees as employee_repo


router = APIRouter()


@router.get("/employee/{id}", response_model=Employee)
def get_employees(id: int, db: Session = Depends(get_db)):
    info = employee_repo.get_employee_by_id(db,id)
    if info is None:
        raise HTTPException(status_code=404, detail="ID doesn't exist, please check the ID.")
    return info


@router.get("/departments/{id}/employees", response_model=list[DepartmentEmployee])
def get_current_employees(id: int, db: Session = Depends(get_db)):
    return employee_repo.get_current_employees_by_department(db, id)
from sqlalchemy.orm import Session
from sqlalchemy import select, text

from aw_api.models.employee import Employee, Department, EmployeeDepartmentHistory

def get_employee_by_id(db: Session, employee_id: int):
    stmt = select(Employee).where(Employee.businessentityid == employee_id)
    return db.execute(stmt).scalar_one_or_none()


def get_current_employees_by_department(db: Session, department_id: int):
    # result = db.execute(
    #     text(
    #         """
    #         SELECT d.name, e.jobtitle, e.hiredate
    #         FROM humanresources.department AS d
    #         JOIN humanresources.employeedepartmenthistory
    #             USING(departmentid)
    #         JOIN humanresources.employee AS e
    #             USING(businessentityid)
    #         WHERE ENDDATE IS null AND departmentid = :departmentid
    #         """
    #     ),
    #     {"departmentid": department_id}
    # )
    # return result.mappings().all()
    
    stmt = (
        select(Department.name, Employee.jobtitle, Employee.hiredate)
        .join(EmployeeDepartmentHistory, EmployeeDepartmentHistory.departmentid == Department.departmentid)
        .join(Employee, Employee.businessentityid == EmployeeDepartmentHistory.businessentityid)
        .where(EmployeeDepartmentHistory.enddate.is_(None))
        .where(Department.departmentid == department_id)
    )
    return db.execute(stmt).mappings().all()
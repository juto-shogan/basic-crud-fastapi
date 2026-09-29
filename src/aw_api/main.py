from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from aw_api.database import get_db
from datetime import date
from pydantic import BaseModel, field_validator
import xml.etree.ElementTree as ET
from typing import Optional

app = FastAPI()

class Employee(BaseModel):
    businessentityid: int
    jobtitle: str
    gender: str
    hiredate: date

class DepartmentEmployee(BaseModel):
    name: str
    jobtitle: str
    hiredate: date

class JobCandidateCreate(BaseModel):
    businessentityid: int
    resume: str
    
    # validating that the variable actually comes as a valid xml
    @field_validator("resume")
    @classmethod
    def resume_must_be_valid_xml(cls, value: str) -> str:
        try:
            ET.fromstring(value)
        except ET.ParseError:
            raise ValueError("resume must be valid XML")
        return value
    
class JobCandidateUpdate(BaseModel):
    resume: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "Hello, AdventureWorks"}


@app.get("/employee/{id}", response_model=Employee)
def get_employees(id: int, db: Session = Depends(get_db)):
    
    result = db.execute(
        text("SELECT * FROM humanresources.employee WHERE businessentityid = :employee_id"),
        {"employee_id": id}
    )
    
    info = result.mappings().first()
    if info is None:
        raise HTTPException(status_code=404, detail="ID doesn't exist, please check the ID")
    else:
        return info


@app.get("/departments/{id}/employees", response_model=list[DepartmentEmployee])
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
    
    info = result.mappings().all()
    return info


@app.post("/jobcandidates")
def create_job_candidate(candidate: JobCandidateCreate, db: Session= Depends(get_db)):
    post = db.execute(
        text(
            """
            INSERT INTO humanresources.jobcandidate (businessentityid, resume)
            VALUES(:businessentityid, :resume)
            """
        ),
        {"businessentityid": candidate.businessentityid,
         "resume": candidate.resume} 
    )
    db.commit()
    return {"message": "Job candidate created successfully"}


@app.delete("/jobcandidates/{id}")
def delete_job_candidate(id: int, db: Session = Depends(get_db)):
    deleting = db.execute(
        text("DELETE FROM humanresources.jobcandidate WHERE jobcandidateid = :jobcandidateid"),
        {"jobcandidateid": id}
    )
    #Attribute "rowcount" is unknown
    if deleting.rowcount == 0: # type: ignore
        raise HTTPException(status_code=404, detail="missing ID")
    else:
        db.commit()
        return {"message": "job candidates deleted successfully"}
    

@app.patch("/jobcandidates/{id}")
def update_job_candidate(id: int, candidate: JobCandidateUpdate, db: Session = Depends(get_db)):
    
    if candidate.resume is not None:
        patching = db.execute(
            text("UPDATE humanresources.jobcandidate SET resume = :resume WHERE jobcandidateid = :jobcandidateid"),
            {"jobcandidateid": id, "resume": candidate.resume}
        )
        
        if patching.rowcount == 0: # type: ignore
            raise HTTPException(status_code=404, detail="missing ID")
        
        db.commit()
        return {"message": "job candidate updated successfully"}
    
    else:
        return {"message": "nothing to update"}
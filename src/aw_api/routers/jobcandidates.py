from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import text

from typing import Optional
from pydantic import BaseModel, field_validator
import xml.etree.ElementTree as ET
from aw_api.database import get_db

router = APIRouter()

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
    

@router.post("/jobcandidates")
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


@router.delete("/jobcandidates/{id}")
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
    

@router.patch("/jobcandidates/{id}")
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
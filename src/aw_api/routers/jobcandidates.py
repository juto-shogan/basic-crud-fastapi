from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import text

from aw_api.database import get_db
from aw_api.schemas.jobcandidates import JobCandidateCreate, JobCandidateUpdate
router = APIRouter()


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
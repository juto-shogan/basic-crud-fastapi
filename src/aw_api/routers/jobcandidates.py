from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import text

from aw_api.database import get_db
from aw_api.schemas.jobcandidates import JobCandidateCreate, JobCandidateUpdate
from aw_api.repositories import jobcandidate as job_repo

router = APIRouter()


@router.post("/jobcandidates")
def create_job_candidates(candidate: JobCandidateCreate, db: Session= Depends(get_db)):
    job_repo.create_job_candidates(
        db,
        candidate.businessentityid,
        candidate.resume
    )
    return {"message": "Job candidate created successfully"}


@router.delete("/jobcandidates/{id}")
def delete_job_candidate(id: int, db: Session = Depends(get_db)):
    
    deleting = job_repo.delete_job_candidate(db, id)
    if not deleting:
        raise HTTPException(status_code=404, detail="missing ID")
    else:
        db.commit()
        return {"message": "job candidates deleted successfully"}
    

@router.patch("/jobcandidates/{id}")
def update_job_candidate(id: int, candidate: JobCandidateUpdate, db: Session = Depends(get_db)):
    
    outcome = job_repo.update_job_candidate_by_id(db, id, candidate.resume)
    if outcome == "no_update":
        return {"message": "nothing to update"}
    
    if outcome == "not_found":
        raise HTTPException(status_code=404, detail="missing ID")
    return {"message": "job candidate updated successfully"}
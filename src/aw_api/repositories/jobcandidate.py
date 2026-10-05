from sqlalchemy.orm import Session
from sqlalchemy import text, insert, delete, update

from aw_api.models.jobcandidate import JobCandidate

def create_job_candidates(
    db: Session,
    businessentityid: int,
    resume: str | None
    ):
    # post = db.execute(
    #     text(
    #         """
    #         INSERT INTO humanresources.jobcandidate (businessentityid, resume)
    #         VALUES(:businessentityid, :resume)
    #         """
    #     ),
    #     {
    #         "businessentityid": businessentityid,
    #         "resume": resume
    #     } 
    # )
    # db.commit()
    stmt = insert(JobCandidate).values(businessentityid=businessentityid, resume=resume)
    db.execute(stmt)
    db.commit()
    

def delete_job_candidate(db: Session, id: int):
    # result = db.execute(
    #     text(
    #     """
    #     DELETE FROM humanresources.jobcandidate
    #     WHERE jobcandidateid = :jobcandidateid
    #     """
    #     ),
    #     {
    #         "jobcandidateid": id
    #     }
    # )
    
    stmt = delete(JobCandidate).where(JobCandidate.jobcandidateid == id)
    result = db.execute(stmt)
    
    # NOTE: Attribute "rowcount" is unknown, thus the ignore below.
    if result.rowcount == 0: # type: ignore
        return False

    db.commit()
    return True


def update_job_candidate_by_id(db: Session, id: int, resume: str | None):
    
    # patching = db.execute(
    #     text(
    #         """
    #         UPDATE humanresources.jobcandidate 
    #         SET resume = :resume 
    #         WHERE jobcandidateid = :jobcandidateid
    #         """
    #     ),
    #     {
    #         "jobcandidateid": id, 
    #         "resume": resume
    #     }
    # )
    
    if resume is None:
        return "no_update"
    
    stmt = update(JobCandidate).where(JobCandidate.jobcandidateid == id).values(resume = resume)
    result = db.execute(stmt)
    
    if result.rowcount == 0: # type: ignore
        return "not_found"
        
    db.commit()
    return "updated"
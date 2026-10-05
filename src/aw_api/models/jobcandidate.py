from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from aw_api.models.base import Base

class JobCandidate(Base):
    __tablename__ = "jobcandidate"
    __table_args__ = {"schema": "humanresources"}
    
    jobcandidateid: Mapped[int] = mapped_column(primary_key=True)
    businessentityid: Mapped[int] = mapped_column(
        ForeignKey("humanresources.employee.businessentityid")
    )
    resume: Mapped[str] = mapped_column(Text)
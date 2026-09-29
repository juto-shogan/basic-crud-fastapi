from pydantic import BaseModel, field_validator
import xml.etree.ElementTree as ET
from typing import Optional

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
from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Optional, Any
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    institution: Optional[str] = None
    bio: Optional[str] = None
    phone_number: Optional[str] = None
    profile_picture: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    institution: Optional[str] = None
    bio: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserStats(BaseModel):
    papers_analyzed: int
    projects_created: int
    notes_written: int

class AnalysisResponse(BaseModel):
    research_topic: str
    extracted_hypotheses: List[str]
    methods_summary: str
    datasets_identified: List[str]
    key_findings: List[str]
    limitations: List[str]
    citation_references: List[str]
    contradictions: Optional[List[str]] = None
    research_gap_identified: str
    suggested_novel_direction: str
    confidence_score: float
    evidence_strength: float
    citation_frequency: float
    methodological_robustness: float

    @field_validator('extracted_hypotheses', 'datasets_identified', 'key_findings', 'limitations', 'citation_references', 'contradictions', mode='before')
    @classmethod
    def coerce_to_list(cls, v):
        if isinstance(v, str):
            return [v] if v.strip() else []
        return v

class PaperHistory(BaseModel):
    id: int
    title: str
    filename: str
    created_at: datetime
    result_json: AnalysisResponse

    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    user_id: int
    created_at: datetime
    papers: List[PaperHistory] = []

    class Config:
        from_attributes = True

class NoteBase(BaseModel):
    content: str

class NoteCreate(NoteBase):
    paper_id: int

class Note(NoteBase):
    id: int
    paper_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

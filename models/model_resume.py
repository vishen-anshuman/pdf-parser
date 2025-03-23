from pydantic import BaseModel


class ResumeModel(BaseModel):
    Id: str
    Name: str
    Education: str
    Experience: str
    Profession: str
    ProfileSummary: str

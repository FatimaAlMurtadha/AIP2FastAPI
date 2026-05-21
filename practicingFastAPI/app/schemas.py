# use pandantic to map ut data in specific situation {POST, UPDAT, GET, ENUMs "STATUS: open, in progress, clsed"}
from enum import Enum
from pydantic import BaseModel, Field # in order to add VALIDATIONS
from typing import Optional # for the optional fields like update

class IssueStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"

class IssuePriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

# the schema for creating issues
class IssueCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100) # validation
    description : str = Field(min_length=5, max_length=1000)
    priority : IssuePriority = IssuePriority.MEDIUM 

class IssueUpdate(BaseModel):
    title : Optional[str] = Field(default=None, max_length=100)
    description : Optional[str] = Field(default=None, max_length=1000)
    priority : Optional [IssuePriority] = None
    status : Optional [IssueStatus] = None


class IssueOut(BaseModel):
    id: str
    title: str
    description: str
    priority: IssuePriority
    status: IssueStatus



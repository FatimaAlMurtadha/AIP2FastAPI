import uuid # since we don't have db
from fastapi import APIRouter, HTTPException, status
from app.schemas import IssueCreate, IssueOut, IssueStatus
from app.storage import load_data, save_data

router = APIRouter(prefix="/api/v1/issues", tags=["issues"])


@router.get("/", response_model=list[IssueOut])
def get_issues():
    issues = load_data()
    return issues

@router.post("/", response_model=IssueOut, status_code=status.HTTP_201_CREATED)
def create_issue(payLoad: IssueCreate):
    """Create a new issue"""
    issues = load_data()

    new_issue = {
        "id" : str(uuid.uuid4()),
        "title" : payLoad.title,
        "description": payLoad.description,
        "priority": payLoad.priority,
        "status" : IssueStatus.OPEN
    }
    issues.append(new_issue)
    save_data(issues)
    return new_issue
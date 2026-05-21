import uuid # since we don't have db
from fastapi import APIRouter, HTTPException, status
from app.schemas import IssueCreate, IssueOut, IssueStatus, IssueUpdate
from app.storage import load_data, save_data

router = APIRouter(prefix="/api/v1/issues", tags=["issues"])

# get all issues
@router.get("/", response_model=list[IssueOut])
def get_issues():
    issues = load_data()
    return issues

# post a new issue
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

# get an issue by its ID
@router.get("/{issue_id}", response_model=IssueOut)
def get_issue(issue_id: str):
    """Retrive a specific issue by ID"""
    issues = load_data()
    for issue in issues:
        if issue["id"] == issue_id:
            return issue
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")

# PUT - update an existing issue
@router.put("/{issue_id}", response_model=IssueOut)
def update_issue(issue_id: str, payload: IssueUpdate):
    """Update an existing issue."""
    issues = load_data()
    for index, issue in enumerate(issues):
        if issue["id"] == issue_id:
            updated_issue = issue.copy()
            if payload.title is not None:
                updated_issue["title"] = payload.title
            if payload.description is not None:
                updated_issue["description"] = payload.description
            if payload.priority is not None:
                updated_issue["priority"] = payload.priority
            if payload.status is not None:
                updated_issue["status"] = payload.status
            issues[index] = update_issue
            save_data(issues)
            return updated_issue
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue that wanted to be updated not found")
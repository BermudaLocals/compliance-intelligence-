from fastapi import APIRouter, HTTPException, Query

from app.schemas.models import (
    Domain,
    DomainCreate,
    Control,
    ControlCreate,
    ControlUpdate,
    Task,
    TaskCreate,
    TaskUpdate,
    ScoreResponse,
)
from app.services.store import store
from app.services.scoring import compute_scores

router = APIRouter()

@router.post("/domains", response_model=Domain)
def create_domain(payload: DomainCreate):
    return store.create_domain(payload)

@router.get("/domains", response_model=list[Domain])
def list_domains():
    return store.list_domains()

@router.post("/controls", response_model=Control)
def create_control(payload: ControlCreate):
    try:
        return store.create_control(payload)
    except ValueError:
        raise HTTPException(status_code=404, detail="domain_not_found")

@router.get("/controls", response_model=list[Control])
def list_controls(domain_id: str | None = Query(default=None)):
    return store.list_controls(domain_id)

@router.patch("/controls/{control_id}", response_model=Control)
def update_control(control_id: str, payload: ControlUpdate):
    try:
        return store.update_control(control_id, payload)
    except ValueError:
        raise HTTPException(status_code=404, detail="control_not_found")

@router.get("/score", response_model=ScoreResponse)
def score():
    return compute_scores()

@router.post("/tasks", response_model=Task)
def create_task(payload: TaskCreate):
    try:
        return store.create_task(payload)
    except ValueError:
        raise HTTPException(status_code=404, detail="control_not_found")

@router.get("/tasks", response_model=list[Task])
def list_tasks(control_id: str | None = Query(default=None)):
    return store.list_tasks(control_id)

@router.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, payload: TaskUpdate):
    try:
        return store.update_task(task_id, payload)
    except ValueError:
        raise HTTPException(status_code=404, detail="task_not_found")

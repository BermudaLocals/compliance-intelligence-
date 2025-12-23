from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException

from app.audit.approval import require_human_approval
from app.audit.logger import log_event
from app.schemas.models import (
    Control,
    ControlCreate,
    ControlUpdate,
    Domain,
    DomainCreate,
    ScoreResponse,
    Task,
    TaskCreate,
    TaskUpdate,
)
from app.services.scoring import compute_scores
from app.services.store import store

router = APIRouter()


def _tenant_id() -> str:
    # Phase 1: static tenant until auth/RBAC is added
    return "tenant_demo"


def _actor() -> str:
    # Phase 1: static actor until auth/RBAC is added
    # IMPORTANT: In production, 'system' will be blocked for guarded actions.
    return "user_demo"


@router.get("/domains", response_model=List[Domain])
def list_domains() -> List[Domain]:
    return store.list_domains()


@router.post("/domains", response_model=Domain)
def create_domain(payload: DomainCreate) -> Domain:
    domain = store.create_domain(payload)

    log_event(
        tenant_id=_tenant_id(),
        actor=_actor(),
        action="CREATE_DOMAIN",
        entity_type="domain",
        entity_id=domain.id,
        after=domain.model_dump(),
    )

    return domain


@router.get("/controls", response_model=List[Control])
def list_controls() -> List[Control]:
    return store.list_controls()


@router.post("/controls", response_model=Control)
def create_control(payload: ControlCreate) -> Control:
    control = store.create_control(payload)

    log_event(
        tenant_id=_tenant_id(),
        actor=_actor(),
        action="CREATE_CONTROL",
        entity_type="control",
        entity_id=control.id,
        after=control.model_dump(),
    )

    return control


@router.patch("/controls/{control_id}", response_model=Control)
def update_control(control_id: str, payload: ControlUpdate) -> Control:
    require_human_approval(_actor(), "UPDATE_CONTROL")

    existing = store.get_control(control_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Control not found")

    before = existing.model_dump()
    updated = store.update_control(control_id, payload)

    log_event(
        tenant_id=_tenant_id(),
        actor=_actor(),
        action="UPDATE_CONTROL",
        entity_type="control",
        entity_id=control_id,
        before=before,
        after=updated.model_dump(),
    )

    return updated


@router.get("/score", response_model=ScoreResponse)
def score() -> ScoreResponse:
    domains = store.list_domains()
    controls = store.list_controls()
    return compute_scores(domains, controls)


@router.get("/tasks", response_model=List[Task])
def list_tasks() -> List[Task]:
    return store.list_tasks()


@router.post("/tasks", response_model=Task)
def create_task(payload: TaskCreate) -> Task:
    task = store.create_task(payload)

    log_event(
        tenant_id=_tenant_id(),
        actor=_actor(),
        action="CREATE_TASK",
        entity_type="task",
        entity_id=task.id,
        after=task.model_dump(),
    )

    return task


@router.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, payload: TaskUpdate) -> Task:
    require_human_approval(_actor(), "UPDATE_TASK")

    existing = store.get_task(task_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Task not found")

    before = existing.model_dump()
    updated = store.update_task(task_id, payload)

    log_event(
        tenant_id=_tenant_id(),
        actor=_actor(),
        action="UPDATE_TASK",
        entity_type="task",
        entity_id=task_id,
        before=before,
        after=updated.model_dump(),
    )

    return updated
from datetime import datetime
from uuid import uuid4

from app.schemas.models import (
    Domain,
    DomainCreate,
    Control,
    ControlCreate,
    ControlUpdate,
    Task,
    TaskCreate,
    TaskUpdate,
)

class InMemoryStore:
    def __init__(self):
        self.domains = {}
        self.controls = {}
        self.tasks = {}

    def create_domain(self, payload: DomainCreate) -> Domain:
        domain = Domain(id=str(uuid4()), **payload.dict())
        self.domains[domain.id] = domain
        return domain

    def list_domains(self):
        return list(self.domains.values())

    def create_control(self, payload: ControlCreate) -> Control:
        if payload.domain_id not in self.domains:
            raise ValueError("domain_not_found")
        control = Control(
            id=str(uuid4()),
            updated_at=datetime.utcnow(),
            **payload.dict(),
        )
        self.controls[control.id] = control
        return control

    def list_controls(self, domain_id=None):
        if domain_id:
            return [c for c in self.controls.values() if c.domain_id == domain_id]
        return list(self.controls.values())

    def update_control(self, control_id, payload: ControlUpdate):
        if control_id not in self.controls:
            raise ValueError("control_not_found")
        control = self.controls[control_id]
        for k, v in payload.dict(exclude_unset=True).items():
            setattr(control, k, v)
        control.updated_at = datetime.utcnow()
        return control

    def create_task(self, payload: TaskCreate):
        if payload.control_id not in self.controls:
            raise ValueError("control_not_found")
        task = Task(
            id=str(uuid4()),
            created_at=datetime.utcnow(),
            is_done=False,
            **payload.dict(),
        )
        self.tasks[task.id] = task
        return task

    def list_tasks(self, control_id=None):
        if control_id:
            return [t for t in self.tasks.values() if t.control_id == control_id]
        return list(self.tasks.values())

    def update_task(self, task_id, payload: TaskUpdate):
        if task_id not in self.tasks:
            raise ValueError("task_not_found")
        task = self.tasks[task_id]
        for k, v in payload.dict(exclude_unset=True).items():
            setattr(task, k, v)
        return task


store = InMemoryStore()

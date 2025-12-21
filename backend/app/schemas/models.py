from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ControlStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"


class DomainCreate(BaseModel):
    name: str
    description: Optional[str] = None


class Domain(DomainCreate):
    id: str


class ControlCreate(BaseModel):
    domain_id: str
    name: str
    description: Optional[str] = None
    weight: float = 1.0
    status: ControlStatus = ControlStatus.UNKNOWN


class Control(ControlCreate):
    id: str
    updated_at: datetime


class ControlUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    weight: Optional[float] = None
    status: Optional[ControlStatus] = None


class TaskCreate(BaseModel):
    control_id: str
    title: str
    description: Optional[str] = None


class Task(TaskCreate):
    id: str
    is_done: bool
    created_at: datetime


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None


class DomainScore(BaseModel):
    domain_id: str
    domain_name: str
    compliance_pct: float
    passed: int
    failed: int
    unknown: int


class ScoreResponse(BaseModel):
    overall_compliance_pct: float
    domains: list[DomainScore]
    updated_at: datetime

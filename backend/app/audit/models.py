from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AuditEvent(BaseModel):
    id: str
    tenant_id: str
    actor: str
    action: str
    entity_type: str
    entity_id: Optional[str] = None

    before: Optional[dict] = None
    after: Optional[dict] = None

    decision: Optional[str] = None
    rationale: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
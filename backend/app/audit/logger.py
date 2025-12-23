import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from app.audit.models import AuditEvent
from app.core.config import settings


AUDIT_DIR = Path(__file__).resolve().parents[2] / "data" / "audit"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

AUDIT_FILE = AUDIT_DIR / "audit.log"


def log_event(
    *,
    tenant_id: str,
    actor: str,
    action: str,
    entity_type: str,
    entity_id: Optional[str] = None,
    before: Optional[dict] = None,
    after: Optional[dict] = None,
    decision: Optional[str] = None,
    rationale: Optional[str] = None,
) -> AuditEvent:
    event = AuditEvent(
        id=str(uuid.uuid4()),
        tenant_id=tenant_id,
        actor=actor,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        before=before,
        after=after,
        decision=decision,
        rationale=rationale,
    )

    record = event.model_dump()
    record["environment"] = settings.environment
    record["created_at"] = datetime.utcnow().isoformat() + "Z"

    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    return event
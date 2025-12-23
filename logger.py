import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from app.audit.models import AuditEvent
from app.core.config import settings


AUDIT_DIR = Path(os.getenv("CI_AUDIT_DIR", Path(__file__).resolve().parents[2] / "data" / "audit"))
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

AUDIT_FILE = AUDIT_DIR / "audit.log"  # append-only JSONL


def _now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


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
    """
    Append-only audit event logger.
    JSONL format: one event per line.
    Advisory platform rule: always log human approvals/declines and any state changes.
    """
    evt = AuditEvent(
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

    record = evt.model_dump()
    record["created_at"] = _now_iso()
    record["environment"] = settings.environment
    record["deployment_mode"] = settings.deployment_mode

    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return evt

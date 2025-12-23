from fastapi import HTTPException
from app.core.config import settings


def require_human_approval(actor: str, action: str) -> None:
    """
    Enforces human-in-loop in production.
    We treat actor == 'system' as non-human.
    """
    if settings.environment == "production" and settings.require_human_approval:
        if actor.lower() in {"system", "bot", "automation"}:
            raise HTTPException(
                status_code=403,
                detail=f"Human approval required for action '{action}' in production.",
            )

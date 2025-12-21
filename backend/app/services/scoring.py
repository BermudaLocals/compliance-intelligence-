from datetime import datetime

from app.schemas.models import ScoreResponse, DomainScore, ControlStatus
from app.services.store import store


def compute_scores() -> ScoreResponse:
    domains = store.list_domains()
    controls = store.list_controls()

    domain_scores = []
    total_pass = total_fail = total_unknown = 0

    for domain in domains:
        d_controls = [c for c in controls if c.domain_id == domain.id]

        passed = sum(1 for c in d_controls if c.status == ControlStatus.PASS)
        failed = sum(1 for c in d_controls if c.status == ControlStatus.FAIL)
        unknown = sum(1 for c in d_controls if c.status == ControlStatus.UNKNOWN)

        total = passed + failed + unknown
        pct = (passed / total) * 100 if total else 0.0

        domain_scores.append(
            DomainScore(
                domain_id=domain.id,
                domain_name=domain.name,
                compliance_pct=round(pct, 2),
                passed=passed,
                failed=failed,
                unknown=unknown,
            )
        )

        total_pass += passed
        total_fail += failed
        total_unknown += unknown

    overall_total = total_pass + total_fail + total_unknown
    overall_pct = (total_pass / overall_total) * 100 if overall_total else 0.0

    return ScoreResponse(
        overall_compliance_pct=round(overall_pct, 2),
        domains=domain_scores,
        updated_at=datetime.utcnow(),
    )

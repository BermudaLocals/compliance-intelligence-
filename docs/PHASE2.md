# PHASE 2 — Compliance Intelligence "Cost Clock + One-Click Remediation"
Owner: John Jefferis
Goal: Make non-compliance understandable + actionable in 60 seconds (CEO mode + IT mode)

## Non-negotiables
- No AML/KYC/IDV/transaction monitoring features.
- ERP integrations remain READ-ONLY (phase later).
- Deterministic, explainable logic only.
- AI is advisory only; system must be reviewable.
- Human-in-loop enforced in production (already in approval gate).
- Audit logging for every state change (already started).

---

## Phase 2 Deliverables (Backend)

### 1) Add "Exposure / Cost Clock" model (deterministic)
We need a simple, explainable exposure estimate:
- daily_cost = (max_fine_usd / grace_days) OR fallback to (max_fine_usd * daily_rate_pct)
- running_total = daily_cost * days_out_of_compliance
- confidence label: low/medium/high (based on data completeness)

Fields to support:
- regulation_name (string)
- max_fine_usd (int)
- fine_type: "per_day" | "per_violation" | "unknown"
- grace_days (int, default 30)
- enforcement_likelihood: 0.0–1.0 (default 0.35; explainable baseline)
- last_changed_at (datetime)
- effective_date (date)
- source_url (string) [optional; phase later can be live feeds]
- notes (string)

IMPORTANT:
- Do NOT claim legal advice.
- Output as "estimated exposure" and "risk indicators suggest".

---

### 2) Add "Remediation Plan" + One-click accept/decline
We need a remediation object tied to controls/tasks:
- remediation_id
- control_id
- recommended_change (structured steps)
- policy_template_patch (text)
- owner_role (CEO/IT/Compliance)
- requires_human_approval (bool default True)
- status: proposed | accepted | declined | implemented
- accepted_at / declined_at
- accepted_by (actor)
- rationale (why accepted/declined)

One click actions:
- POST /v1/remediations/{id}/accept
- POST /v1/remediations/{id}/decline
- POST /v1/remediations/{id}/implement  (phase 2.5; can be stub = creates tasks)

Every click must:
- enforce require_human_approval (production)
- write audit log event with before/after and decision+rationale

---

### 3) Add "CEO View" vs "Deep View" (API)
CEO view returns:
- overall compliance %
- top 5 highest exposure items
- newest changes (last 24–72 hours; using last_changed_at)
- "Ray Charles mode": simple status lights (green/yellow/red) + $ running total

Deep view returns:
- per domain breakdown
- per control breakdown
- task backlog and ownership
- audit trail pointers

Endpoints:
- GET /v1/dashboard/ceo
- GET /v1/dashboard/deep

No frontend yet; backend must return JSON that a UI can render.

---

### 4) Add "Reg change tracker" (manual now, live feed later)
Create a simple in-app registry of "Regulatory Updates" (manual input for now):
- update_id
- title
- summary
- effective_date
- last_changed_at
- impacted_domains [list]
- impacted_controls [list]
- recommended_actions [list strings]
- severity: low/med/high

Endpoints:
- POST /v1/updates
- GET /v1/updates
- GET /v1/updates/recent?days=3

Audit log required for create/update.

---

### 5) Add Read-only Audit endpoint (enterprise expectation)
- GET /v1/audit?limit=100 (reads JSONL audit log)
- Must be read-only and never mutate
- Return newest-first
- Do not expose secrets

---

## Implementation Notes
- We are still using in-memory store (services/store.py). Keep it consistent for Phase 2.
- Add schemas in app/schemas/models.py (Pydantic models).
- Add store methods for remediations + updates.
- Add deterministic functions in app/services/exposure.py and app/services/remediation.py
- Keep imports stable: scoring function is compute_scores().
- Do NOT write .pyc files to git; confirm .gitignore includes __pycache__/ and *.pyc.

---

## Definition of Done
- /docs shows CEO + deep endpoints
- You can create a control as non-compliant + attach max_fine_usd
- /v1/dashboard/ceo shows a running exposure number
- Accept/decline remediation creates an audit log entry
- /v1/audit returns audit events newest-first

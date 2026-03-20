"""Action handler seed for adjustment_entry:post."""

from __future__ import annotations

from typing import Any, cast


DOC_ID = "adjustment_entry"
ACTION_ID = "post"
ACTION_RULE: dict[str, Any] = {'allowed_in_states': ['draft', 'approved', 'posted'], 'transitions_to': None}

STATE_FIELD = 'workflow_state'
WORKFLOW_HINTS = {'business_objective': 'collect accounting records for a reporting period, generate financial statements, review them, and publish management-ready financial outputs', 'actors': ['finance controller', 'reporting accountant', 'approver', 'management audience'], 'start_condition': 'a reporting period is ready for statement preparation', 'ordered_steps': ['Collect postings and prepare required adjustments.'], 'primary_actions': ['review', 'create', 'approve', 'post'], 'primary_transitions': ['adjustment_entry: draft -> approved -> posted'], 'downstream_effects': ['feeds management reporting, audit, compliance, and executive decision-making'], 'action_actors': {'create': ['finance controller'], 'review': ['reporting accountant'], 'approve': ['approver'], 'post': ['finance controller'], 'reverse': ['finance controller'], 'archive': ['finance controller']}}

def handle_post(payload: dict, context: dict | None = None) -> dict:
    context = context or {}
    next_state = cast(str | None, ACTION_RULE.get("transitions_to"))
    updates = {STATE_FIELD: next_state} if STATE_FIELD and next_state else {}
    return {
        "doc_id": DOC_ID,
        "action_id": ACTION_ID,
        "payload": payload,
        "context": context,
        "allowed_in_states": ACTION_RULE.get("allowed_in_states", []),
        "next_state": next_state,
        "updates": updates,
        "workflow_objective": WORKFLOW_HINTS.get("business_objective"),
    }

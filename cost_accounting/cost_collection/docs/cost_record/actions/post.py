"""Action handler seed for cost_record:post."""

from __future__ import annotations

from typing import Any, cast


DOC_ID = "cost_record"
ACTION_ID = "post"
ACTION_RULE: dict[str, Any] = {'allowed_in_states': ['draft', 'reviewed', 'allocated', 'posted'], 'transitions_to': None}

STATE_FIELD = 'workflow_state'
WORKFLOW_HINTS = {'relation_context': {'related_docs': ['cost_center', 'cost_allocation_rule', 'variance_record', 'journal_entry'], 'borrowed_fields': ['target centers', 'allocation basis from linked rules'], 'inferred_roles': ['finance officer']}, 'actors': ['finance officer'], 'action_actors': {'create': ['finance officer'], 'review': ['finance officer'], 'post': ['finance officer'], 'archive': ['finance officer']}}

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

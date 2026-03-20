"""Action handler seed for ar_aging_snapshot:review."""

from __future__ import annotations

from typing import Any, cast


DOC_ID = "ar_aging_snapshot"
ACTION_ID = "review"
ACTION_RULE: dict[str, Any] = {'allowed_in_states': ['active'], 'transitions_to': None}

STATE_FIELD = 'workflow_state'
WORKFLOW_HINTS = {'relation_context': {'related_docs': ['customer_invoice', 'customer_account'], 'borrowed_fields': ['customer identity from customer_account', 'due balances from customer_invoice'], 'inferred_roles': ['account owner', 'finance officer']}, 'actors': ['account owner', 'finance officer'], 'action_actors': {'create': ['account owner'], 'review': ['finance officer'], 'archive': ['account owner']}}

def handle_review(payload: dict, context: dict | None = None) -> dict:
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

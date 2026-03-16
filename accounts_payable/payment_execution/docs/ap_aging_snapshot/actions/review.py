"""Action handler seed for ap_aging_snapshot:review."""

from __future__ import annotations


DOC_ID = "ap_aging_snapshot"
ACTION_ID = "review"
ACTION_RULE = {'allowed_in_states': ['active'], 'transitions_to': None}

STATE_FIELD = 'workflow_state'
WORKFLOW_HINTS = {'relation_context': {'related_docs': ['supplier_invoice', 'supplier_profile'], 'borrowed_fields': ['supplier identity from supplier_profile', 'outstanding balances from supplier_invoice'], 'inferred_roles': ['procurement officer', 'finance officer']}, 'actors': ['procurement officer', 'finance officer'], 'action_actors': {'create': ['procurement officer'], 'review': ['finance officer'], 'archive': ['procurement officer']}}

def handle_review(payload: dict, context: dict | None = None) -> dict:
    context = context or {}
    next_state = ACTION_RULE.get("transitions_to")
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

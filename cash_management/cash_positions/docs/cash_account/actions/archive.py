"""Action handler seed for cash_account:archive."""

from __future__ import annotations


DOC_ID = "cash_account"
ACTION_ID = "archive"
ACTION_RULE = {'allowed_in_states': ['active'], 'transitions_to': 'archived'}

STATE_FIELD = 'workflow_state'
WORKFLOW_HINTS = {'relation_context': {'related_docs': ['receipt_record', 'supplier_payment', 'bank_reconciliation', 'treasury_movement'], 'borrowed_fields': ['institution metadata from bank integration docs where applicable'], 'inferred_roles': ['procurement officer', 'finance officer']}, 'actors': ['procurement officer', 'finance officer'], 'action_actors': {'create': ['procurement officer'], 'update': ['procurement officer'], 'review': ['finance officer'], 'archive': ['procurement officer']}}

def handle_archive(payload: dict, context: dict | None = None) -> dict:
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

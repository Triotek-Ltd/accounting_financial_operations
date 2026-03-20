"""Action handler seed for payment_request:reject."""

from __future__ import annotations

from typing import Any, cast


DOC_ID = "payment_request"
ACTION_ID = "reject"
ACTION_RULE: dict[str, Any] = {'allowed_in_states': ['draft', 'submitted', 'approved', 'executed', 'cancelled'], 'transitions_to': None}

STATE_FIELD = 'workflow_state'
WORKFLOW_HINTS = {'business_objective': 'receive supplier invoices, verify them against procurement evidence, approve them, pay them, and keep the payable ledger current', 'actors': ['AP clerk', 'reviewer', 'approver', 'treasury or finance officer'], 'start_condition': 'a supplier invoice is received', 'ordered_steps': ['Raise and approve the payment request.', 'Archive invoice and payment evidence.'], 'primary_actions': ['create', 'submit', 'review', 'approve', 'execute', 'archive'], 'primary_transitions': ['payment_request: draft -> submitted -> approved -> executed'], 'downstream_effects': ['updates AP aging, cash management, bookkeeping, and supplier history'], 'action_actors': {'create': ['AP clerk'], 'submit': ['AP clerk'], 'review': ['reviewer'], 'approve': ['approver'], 'reject': ['approver'], 'execute': ['treasury or finance officer'], 'cancel': ['AP clerk', 'approver'], 'archive': ['AP clerk']}}

def handle_reject(payload: dict, context: dict | None = None) -> dict:
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

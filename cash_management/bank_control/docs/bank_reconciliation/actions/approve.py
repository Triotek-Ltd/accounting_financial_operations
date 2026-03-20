"""Action handler seed for bank_reconciliation:approve."""

from __future__ import annotations

from typing import Any, cast


DOC_ID = "bank_reconciliation"
ACTION_ID = "approve"
ACTION_RULE: dict[str, Any] = {'allowed_in_states': ['open', 'matching', 'balanced', 'approved'], 'transitions_to': 'approved'}

STATE_FIELD = 'workflow_state'
WORKFLOW_HINTS = {'relation_context': {'related_docs': ['cash_account', 'receipt_record', 'supplier_payment', 'journal_entry'], 'borrowed_fields': ['account details from cash_account', 'transaction refs from linked receipts/payments'], 'inferred_roles': ['procurement officer', 'finance officer']}, 'actors': ['procurement officer', 'finance officer'], 'action_actors': {'create': ['procurement officer'], 'review': ['finance officer'], 'approve': ['finance officer'], 'close': ['procurement officer'], 'archive': ['procurement officer']}}

def handle_approve(payload: dict, context: dict | None = None) -> dict:
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

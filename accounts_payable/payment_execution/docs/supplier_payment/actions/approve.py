"""Action handler seed for supplier_payment:approve."""

from __future__ import annotations


DOC_ID = "supplier_payment"
ACTION_ID = "approve"
ACTION_RULE = {'allowed_in_states': ['draft', 'approved', 'posted', 'reconciled'], 'transitions_to': 'approved'}

STATE_FIELD = 'workflow_state'
WORKFLOW_HINTS = {'business_objective': 'receive supplier invoices, verify them against procurement evidence, approve them, pay them, and keep the payable ledger current', 'actors': ['AP clerk', 'reviewer', 'approver', 'treasury or finance officer'], 'start_condition': 'a supplier invoice is received', 'ordered_steps': ['Execute supplier payment.', 'Reconcile payment against invoice balances.', 'Archive invoice and payment evidence.'], 'primary_actions': ['create', 'review', 'approve', 'post', 'reconcile', 'reverse', 'archive'], 'primary_transitions': ['supplier_payment: draft -> approved -> posted', 'supplier_payment: posted -> reconciled'], 'downstream_effects': ['updates AP aging, cash management, bookkeeping, and supplier history'], 'action_actors': {'create': ['AP clerk'], 'review': ['reviewer'], 'approve': ['approver'], 'post': ['treasury or finance officer'], 'reconcile': ['treasury or finance officer'], 'reverse': ['approver'], 'archive': ['AP clerk']}}

def handle_approve(payload: dict, context: dict | None = None) -> dict:
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

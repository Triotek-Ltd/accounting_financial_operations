"""Action handler seed for receipt_record:approve."""

from __future__ import annotations


DOC_ID = "receipt_record"
ACTION_ID = "approve"
ACTION_RULE = {'allowed_in_states': ['draft', 'approved', 'posted', 'reconciled'], 'transitions_to': 'approved'}

STATE_FIELD = 'workflow_state'
WORKFLOW_HINTS = {'business_objective': 'bill customers, track outstanding balances, collect payment, and maintain accurate receivable balances', 'actors': ['billing officer', 'collections officer', 'customer-facing finance team'], 'start_condition': 'a sales transaction is ready for billing', 'ordered_steps': ['Receive and record customer payment.', 'Reconcile receipts to invoices and customer balances.'], 'primary_actions': ['create', 'review', 'approve', 'post', 'reconcile'], 'primary_transitions': ['receipt_record: draft -> approved -> posted', 'receipt_record: posted -> reconciled'], 'downstream_effects': ['updates AR aging, customer history, cash management, and bookkeeping']}

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

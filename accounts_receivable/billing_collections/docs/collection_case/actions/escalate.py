"""Action handler seed for collection_case:escalate."""

from __future__ import annotations


DOC_ID = "collection_case"
ACTION_ID = "escalate"
ACTION_RULE = {'allowed_in_states': ['open', 'contacted', 'promised', 'escalated', 'resolved'], 'transitions_to': 'escalated'}

STATE_FIELD = 'workflow_state'
WORKFLOW_HINTS = {'business_objective': 'bill customers, track outstanding balances, collect payment, and maintain accurate receivable balances', 'actors': ['billing officer', 'collections officer', 'customer-facing finance team'], 'start_condition': 'a sales transaction is ready for billing', 'ordered_steps': ['Monitor outstanding balances and chase overdue items.', 'Close collection activity when settled.'], 'primary_actions': ['create', 'assign', 'contact', 'escalate', 'resolve', 'close', 'archive'], 'primary_transitions': ['collection_case: opened -> contacted -> promised or escalated -> resolved -> closed'], 'downstream_effects': ['updates AR aging, customer history, cash management, and bookkeeping']}

def handle_escalate(payload: dict, context: dict | None = None) -> dict:
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

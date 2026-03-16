"""Action handler seed for customer_invoice:archive."""

from __future__ import annotations


DOC_ID = "customer_invoice"
ACTION_ID = "archive"
ACTION_RULE = {'allowed_in_states': ['draft', 'approved', 'unpaid', 'partially_paid'], 'transitions_to': 'archived'}

STATE_FIELD = 'workflow_state'
WORKFLOW_HINTS = {'business_objective': 'bill customers, track outstanding balances, collect payment, and maintain accurate receivable balances', 'actors': ['billing officer', 'collections officer', 'customer-facing finance team'], 'start_condition': 'a sales transaction is ready for billing', 'ordered_steps': ['Create and approve the customer invoice.', 'Record receivable and send invoice to the customer.', 'Reconcile receipts to invoices and customer balances.'], 'primary_actions': ['create', 'update', 'review', 'approve', 'issue', 'post', 'reconcile'], 'primary_transitions': ['customer_invoice: draft -> approved -> unpaid', 'customer_invoice: unpaid -> partially_paid or paid'], 'downstream_effects': ['updates AR aging, customer history, cash management, and bookkeeping'], 'action_actors': {'create': ['billing officer'], 'update': ['billing officer'], 'review': ['collections officer'], 'approve': ['collections officer'], 'post': ['customer-facing finance team'], 'issue': ['billing officer'], 'archive': ['billing officer']}}

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

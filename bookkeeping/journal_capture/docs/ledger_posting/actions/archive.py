"""Action handler seed for ledger_posting:archive."""

from __future__ import annotations


DOC_ID = "ledger_posting"
ACTION_ID = "archive"
ACTION_RULE = {'allowed_in_states': ['active'], 'transitions_to': 'archived'}

STATE_FIELD = 'workflow_state'
WORKFLOW_HINTS = {'business_objective': 'validate financial transaction evidence, capture journals, post ledger entries, and retain auditable accounting records', 'actors': ['accounting officer', 'reviewer', 'approver', 'finance controller'], 'start_condition': 'a financial transaction or adjustment requires accounting recognition', 'ordered_steps': ['Record debit and credit ledger postings.', 'Post the journal to the ledger.', 'Reconcile or reverse if errors are found.', 'Retain the accounting record set for audit and reporting.'], 'primary_actions': ['record', 'review', 'post', 'reverse', 'archive'], 'primary_transitions': ['ledger_posting: active', 'ledger_posting: active -> reversed'], 'downstream_effects': ['postings feed reporting, reconciliation, receivables, payables, and closing workflows']}

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

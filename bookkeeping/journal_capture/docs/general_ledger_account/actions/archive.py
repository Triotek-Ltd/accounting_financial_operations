"""Action handler seed for general_ledger_account:archive."""

from __future__ import annotations


DOC_ID = "general_ledger_account"
ACTION_ID = "archive"
ACTION_RULE = {'allowed_in_states': ['active', 'disabled'], 'transitions_to': 'archived'}

STATE_FIELD = 'workflow_state'
WORKFLOW_HINTS = {'business_objective': 'validate financial transaction evidence, capture journals, post ledger entries, and retain auditable accounting records', 'actors': ['accounting officer', 'reviewer', 'approver', 'finance controller'], 'start_condition': 'a financial transaction or adjustment requires accounting recognition', 'ordered_steps': ['Receive transaction evidence and classify the transaction.', 'Validate supporting documentation and account mapping.'], 'primary_actions': ['create', 'update', 'review', 'approve'], 'primary_transitions': [], 'downstream_effects': ['postings feed reporting, reconciliation, receivables, payables, and closing workflows'], 'action_actors': {'create': ['accounting officer'], 'update': ['accounting officer'], 'review': ['reviewer'], 'archive': ['accounting officer']}}

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

"""Action handler seed for supplier_invoice:archive."""

from __future__ import annotations


DOC_ID = "supplier_invoice"
ACTION_ID = "archive"
ACTION_RULE = {'allowed_in_states': ['draft', 'approved', 'payable', 'partially_paid'], 'transitions_to': 'archived'}

STATE_FIELD = 'workflow_state'
WORKFLOW_HINTS = {'business_objective': 'receive supplier invoices, verify them against procurement evidence, approve them, pay them, and keep the payable ledger current', 'actors': ['AP clerk', 'reviewer', 'approver', 'treasury or finance officer'], 'start_condition': 'a supplier invoice is received', 'ordered_steps': ['Capture the supplier invoice and basic terms.', 'Match invoice against purchase and receipt records.', 'Reconcile payment against invoice balances.', 'Archive invoice and payment evidence.'], 'primary_actions': ['create', 'update', 'review', 'approve', 'reconcile', 'mark_payable', 'archive'], 'primary_transitions': ['supplier_invoice: draft', 'supplier_invoice: draft -> approved -> payable', 'supplier_invoice: payable -> partially_paid or paid'], 'downstream_effects': ['updates AP aging, cash management, bookkeeping, and supplier history']}

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

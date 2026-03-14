"""Action handler seed for financial_statement_run:review."""

from __future__ import annotations


DOC_ID = "financial_statement_run"
ACTION_ID = "review"
ACTION_RULE = {'allowed_in_states': ['draft', 'generated', 'reviewed', 'approved', 'published'], 'transitions_to': 'reviewed'}

STATE_FIELD = 'workflow_state'
WORKFLOW_HINTS = {'business_objective': 'collect accounting records for a reporting period, generate financial statements, review them, and publish management-ready financial outputs', 'actors': ['finance controller', 'reporting accountant', 'approver', 'management audience'], 'start_condition': 'a reporting period is ready for statement preparation', 'ordered_steps': ['Create the statement generation run.', 'Review, approve, and publish the statement set.'], 'primary_actions': ['create', 'generate', 'review', 'approve', 'publish'], 'primary_transitions': ['financial_statement_run: draft -> generated', 'financial_statement_run: generated -> reviewed -> approved -> published'], 'downstream_effects': ['feeds management reporting, audit, compliance, and executive decision-making']}

def handle_review(payload: dict, context: dict | None = None) -> dict:
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

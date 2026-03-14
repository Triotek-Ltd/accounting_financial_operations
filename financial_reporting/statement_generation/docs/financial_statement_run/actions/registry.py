"""Action registry seed for financial_statement_run."""

from __future__ import annotations


DOC_ID = "financial_statement_run"
ALLOWED_ACTIONS = ['create', 'generate', 'review', 'approve', 'publish', 'archive']
ACTION_RULES = {'create': {'allowed_in_states': ['draft', 'generated', 'reviewed', 'approved', 'published'], 'transitions_to': None}, 'generate': {'allowed_in_states': ['draft', 'generated', 'reviewed', 'approved', 'published'], 'transitions_to': None}, 'review': {'allowed_in_states': ['draft', 'generated', 'reviewed', 'approved', 'published'], 'transitions_to': 'reviewed'}, 'approve': {'allowed_in_states': ['draft', 'generated', 'reviewed', 'approved', 'published'], 'transitions_to': 'approved'}, 'publish': {'allowed_in_states': ['draft', 'generated', 'reviewed', 'approved', 'published'], 'transitions_to': 'published'}, 'archive': {'allowed_in_states': ['draft', 'generated', 'reviewed', 'approved', 'published'], 'transitions_to': 'archived'}}

STATE_FIELD = 'workflow_state'

def get_action_handler_name(action_id: str) -> str:
    return f"handle_{action_id}"

def get_action_module_path(action_id: str) -> str:
    return f"actions/{action_id}.py"

def action_contract(action_id: str) -> dict:
    return {
        "state_field": STATE_FIELD,
        "rule": ACTION_RULES.get(action_id, {}),
    }

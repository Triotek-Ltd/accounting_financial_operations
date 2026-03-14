"""Action registry seed for journal_entry."""

from __future__ import annotations


DOC_ID = "journal_entry"
ALLOWED_ACTIONS = ['create', 'update', 'review', 'approve', 'post', 'reverse', 'archive']
ACTION_RULES = {'create': {'allowed_in_states': ['draft', 'reviewed', 'approved', 'posted'], 'transitions_to': None}, 'update': {'allowed_in_states': ['draft', 'reviewed', 'approved', 'posted'], 'transitions_to': None}, 'review': {'allowed_in_states': ['draft', 'reviewed', 'approved', 'posted'], 'transitions_to': 'reviewed'}, 'approve': {'allowed_in_states': ['draft', 'reviewed', 'approved', 'posted'], 'transitions_to': 'approved'}, 'post': {'allowed_in_states': ['draft', 'reviewed', 'approved', 'posted'], 'transitions_to': None}, 'reverse': {'allowed_in_states': ['draft', 'reviewed', 'approved', 'posted'], 'transitions_to': 'reversed'}, 'archive': {'allowed_in_states': ['draft', 'reviewed', 'approved', 'posted'], 'transitions_to': 'archived'}}

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

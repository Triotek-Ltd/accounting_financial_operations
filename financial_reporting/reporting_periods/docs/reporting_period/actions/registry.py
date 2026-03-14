"""Action registry seed for reporting_period."""

from __future__ import annotations


DOC_ID = "reporting_period"
ALLOWED_ACTIONS = ['create', 'update', 'open', 'close', 'archive']
ACTION_RULES = {'create': {'allowed_in_states': ['planned', 'open', 'closing'], 'transitions_to': None}, 'update': {'allowed_in_states': ['planned', 'open', 'closing'], 'transitions_to': None}, 'open': {'allowed_in_states': ['planned', 'open', 'closing'], 'transitions_to': None}, 'close': {'allowed_in_states': ['planned', 'open', 'closing'], 'transitions_to': 'closed'}, 'archive': {'allowed_in_states': ['planned', 'open', 'closing'], 'transitions_to': 'archived'}}

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

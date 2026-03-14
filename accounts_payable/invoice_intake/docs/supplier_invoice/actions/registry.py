"""Action registry seed for supplier_invoice."""

from __future__ import annotations


DOC_ID = "supplier_invoice"
ALLOWED_ACTIONS = ['create', 'update', 'review', 'approve', 'post', 'mark_payable', 'archive']
ACTION_RULES = {'create': {'allowed_in_states': ['draft', 'approved', 'payable', 'partially_paid'], 'transitions_to': None}, 'update': {'allowed_in_states': ['draft', 'approved', 'payable', 'partially_paid'], 'transitions_to': None}, 'review': {'allowed_in_states': ['draft', 'approved', 'payable', 'partially_paid'], 'transitions_to': None}, 'approve': {'allowed_in_states': ['draft', 'approved', 'payable', 'partially_paid'], 'transitions_to': 'approved'}, 'post': {'allowed_in_states': ['draft', 'approved', 'payable', 'partially_paid'], 'transitions_to': None}, 'mark_payable': {'allowed_in_states': ['draft', 'approved', 'payable', 'partially_paid'], 'transitions_to': None}, 'archive': {'allowed_in_states': ['draft', 'approved', 'payable', 'partially_paid'], 'transitions_to': 'archived'}}

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

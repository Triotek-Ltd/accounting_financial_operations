"""Workflow service seed for supplier_invoice."""

from __future__ import annotations

from typing import Any, cast


DOC_ID = "supplier_invoice"
ARCHETYPE = "transaction"
INITIAL_STATE = 'draft'
STATES = ['draft', 'approved', 'payable', 'partially_paid', 'paid', 'archived']
TERMINAL_STATES = ['paid', 'archived']
ACTION_RULES: dict[str, dict[str, Any]] = {'create': {'allowed_in_states': ['draft', 'approved', 'payable', 'partially_paid'], 'transitions_to': None}, 'update': {'allowed_in_states': ['draft', 'approved', 'payable', 'partially_paid'], 'transitions_to': None}, 'review': {'allowed_in_states': ['draft', 'approved', 'payable', 'partially_paid'], 'transitions_to': None}, 'approve': {'allowed_in_states': ['draft', 'approved', 'payable', 'partially_paid'], 'transitions_to': 'approved'}, 'post': {'allowed_in_states': ['draft', 'approved', 'payable', 'partially_paid'], 'transitions_to': None}, 'mark_payable': {'allowed_in_states': ['draft', 'approved', 'payable', 'partially_paid'], 'transitions_to': None}, 'archive': {'allowed_in_states': ['draft', 'approved', 'payable', 'partially_paid'], 'transitions_to': 'archived'}}

STATE_FIELD = 'workflow_state'
WORKFLOW_HINTS = {'business_objective': 'receive supplier invoices, verify them against procurement evidence, approve them, pay them, and keep the payable ledger current', 'actors': ['AP clerk', 'reviewer', 'approver', 'treasury or finance officer'], 'start_condition': 'a supplier invoice is received', 'ordered_steps': ['Capture the supplier invoice and basic terms.', 'Match invoice against purchase and receipt records.', 'Reconcile payment against invoice balances.', 'Archive invoice and payment evidence.'], 'primary_actions': ['create', 'update', 'review', 'approve', 'reconcile', 'mark_payable', 'archive'], 'primary_transitions': ['supplier_invoice: draft', 'supplier_invoice: draft -> approved -> payable', 'supplier_invoice: payable -> partially_paid or paid'], 'downstream_effects': ['updates AP aging, cash management, bookkeeping, and supplier history'], 'action_actors': {'create': ['AP clerk'], 'update': ['AP clerk'], 'review': ['reviewer'], 'approve': ['approver'], 'post': ['treasury or finance officer'], 'archive': ['AP clerk']}}

class WorkflowService:
    def allowed_actions_for_state(self, state: str | None) -> list[str]:
        if not state:
            return list(ACTION_RULES.keys())
        allowed = []
        for action_id, rule in ACTION_RULES.items():
            states = rule.get("allowed_in_states") or []
            if not states or state in states:
                allowed.append(action_id)
        return allowed

    def is_action_allowed(self, action_id: str, state: str | None) -> bool:
        return action_id in self.allowed_actions_for_state(state)

    def next_state_for(self, action_id: str) -> str | None:
        rule = ACTION_RULES.get(action_id, {})
        return cast(str | None, rule.get("transitions_to"))

    def apply_action(self, action_id: str, state: str | None) -> dict:
        if not self.is_action_allowed(action_id, state):
            raise ValueError(f"Action '{action_id}' is not allowed in state '{state}'")
        next_state = self.next_state_for(action_id)
        updates = {STATE_FIELD: next_state} if STATE_FIELD and next_state else {}
        return {
            "action_id": action_id,
            "current_state": state,
            "next_state": next_state,
            "updates": updates,
        }

    def is_terminal(self, state: str | None) -> bool:
        return bool(state and state in TERMINAL_STATES)

    def workflow_summary(self) -> dict:
        return {
            "initial_state": INITIAL_STATE,
            "states": STATES,
            "terminal_states": TERMINAL_STATES,
            "business_objective": WORKFLOW_HINTS.get("business_objective"),
            "ordered_steps": WORKFLOW_HINTS.get("ordered_steps", []),
        }

    def workflow_profile(self) -> dict:
        return {'mode': 'transaction_flow', 'supports_submission': True}

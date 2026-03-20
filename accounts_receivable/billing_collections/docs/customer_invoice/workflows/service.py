"""Workflow service seed for customer_invoice."""

from __future__ import annotations

from typing import Any, cast


DOC_ID = "customer_invoice"
ARCHETYPE = "transaction"
INITIAL_STATE = 'draft'
STATES = ['draft', 'approved', 'unpaid', 'partially_paid', 'paid', 'archived']
TERMINAL_STATES = ['paid', 'archived']
ACTION_RULES: dict[str, dict[str, Any]] = {'create': {'allowed_in_states': ['draft', 'approved', 'unpaid', 'partially_paid'], 'transitions_to': None}, 'update': {'allowed_in_states': ['draft', 'approved', 'unpaid', 'partially_paid'], 'transitions_to': None}, 'review': {'allowed_in_states': ['draft', 'approved', 'unpaid', 'partially_paid'], 'transitions_to': None}, 'approve': {'allowed_in_states': ['draft', 'approved', 'unpaid', 'partially_paid'], 'transitions_to': 'approved'}, 'post': {'allowed_in_states': ['draft', 'approved', 'unpaid', 'partially_paid'], 'transitions_to': None}, 'issue': {'allowed_in_states': ['approved'], 'transitions_to': 'unpaid'}, 'archive': {'allowed_in_states': ['draft', 'approved', 'unpaid', 'partially_paid'], 'transitions_to': 'archived'}}

STATE_FIELD = 'workflow_state'
WORKFLOW_HINTS = {'business_objective': 'bill customers, track outstanding balances, collect payment, and maintain accurate receivable balances', 'actors': ['billing officer', 'collections officer', 'customer-facing finance team'], 'start_condition': 'a sales transaction is ready for billing', 'ordered_steps': ['Create and approve the customer invoice.', 'Record receivable and send invoice to the customer.', 'Reconcile receipts to invoices and customer balances.'], 'primary_actions': ['create', 'update', 'review', 'approve', 'issue', 'post', 'reconcile'], 'primary_transitions': ['customer_invoice: draft -> approved -> unpaid', 'customer_invoice: unpaid -> partially_paid or paid'], 'downstream_effects': ['updates AR aging, customer history, cash management, and bookkeeping'], 'action_actors': {'create': ['billing officer'], 'update': ['billing officer'], 'review': ['collections officer'], 'approve': ['collections officer'], 'post': ['customer-facing finance team'], 'issue': ['billing officer'], 'archive': ['billing officer']}}

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

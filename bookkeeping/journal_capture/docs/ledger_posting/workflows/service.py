"""Workflow service seed for ledger_posting."""

from __future__ import annotations


DOC_ID = "ledger_posting"
ARCHETYPE = "ledger"
INITIAL_STATE = 'active'
STATES = ['active', 'reversed', 'archived']
TERMINAL_STATES = ['reversed', 'archived']
ACTION_RULES = {'record': {'allowed_in_states': ['active'], 'transitions_to': None}, 'review': {'allowed_in_states': ['active'], 'transitions_to': None}, 'reverse': {'allowed_in_states': ['active'], 'transitions_to': 'reversed'}, 'archive': {'allowed_in_states': ['active'], 'transitions_to': 'archived'}}

STATE_FIELD = 'workflow_state'
WORKFLOW_HINTS = {'business_objective': 'validate financial transaction evidence, capture journals, post ledger entries, and retain auditable accounting records', 'actors': ['accounting officer', 'reviewer', 'approver', 'finance controller'], 'start_condition': 'a financial transaction or adjustment requires accounting recognition', 'ordered_steps': ['Record debit and credit ledger postings.', 'Post the journal to the ledger.', 'Reconcile or reverse if errors are found.', 'Retain the accounting record set for audit and reporting.'], 'primary_actions': ['record', 'review', 'post', 'reverse', 'archive'], 'primary_transitions': ['ledger_posting: active', 'ledger_posting: active -> reversed'], 'downstream_effects': ['postings feed reporting, reconciliation, receivables, payables, and closing workflows']}

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
        return rule.get("transitions_to")

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
        return {'mode': 'posting_flow', 'supports_reconciliation': True}

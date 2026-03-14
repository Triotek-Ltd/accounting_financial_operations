"""Workflow service seed for collection_case."""

from __future__ import annotations


DOC_ID = "collection_case"
ARCHETYPE = "workflow_case"
INITIAL_STATE = 'open'
STATES = ['open', 'contacted', 'promised', 'escalated', 'resolved', 'closed', 'archived']
TERMINAL_STATES = ['closed', 'archived']
ACTION_RULES = {'create': {'allowed_in_states': ['open', 'contacted', 'promised', 'escalated', 'resolved'], 'transitions_to': None}, 'assign': {'allowed_in_states': ['open', 'contacted', 'promised', 'escalated', 'resolved'], 'transitions_to': None}, 'contact': {'allowed_in_states': ['open', 'contacted', 'promised', 'escalated', 'resolved'], 'transitions_to': None}, 'escalate': {'allowed_in_states': ['open', 'contacted', 'promised', 'escalated', 'resolved'], 'transitions_to': 'escalated'}, 'resolve': {'allowed_in_states': ['open', 'contacted', 'promised', 'escalated', 'resolved'], 'transitions_to': 'resolved'}, 'close': {'allowed_in_states': ['open', 'contacted', 'promised', 'escalated', 'resolved'], 'transitions_to': 'closed'}, 'archive': {'allowed_in_states': ['open', 'contacted', 'promised', 'escalated', 'resolved'], 'transitions_to': 'archived'}}

STATE_FIELD = 'workflow_state'
WORKFLOW_HINTS = {'business_objective': 'bill customers, track outstanding balances, collect payment, and maintain accurate receivable balances', 'actors': ['billing officer', 'collections officer', 'customer-facing finance team'], 'start_condition': 'a sales transaction is ready for billing', 'ordered_steps': ['Monitor outstanding balances and chase overdue items.', 'Close collection activity when settled.'], 'primary_actions': ['create', 'assign', 'contact', 'escalate', 'resolve', 'close', 'archive'], 'primary_transitions': ['collection_case: opened -> contacted -> promised or escalated -> resolved -> closed'], 'downstream_effects': ['updates AR aging, customer history, cash management, and bookkeeping']}

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
        return {'mode': 'case_flow', 'supports_assignment': True, 'supports_escalation': True}

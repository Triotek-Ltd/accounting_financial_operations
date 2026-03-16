"""Workflow service seed for reporting_period."""

from __future__ import annotations


DOC_ID = "reporting_period"
ARCHETYPE = "configuration"
INITIAL_STATE = 'planned'
STATES = ['planned', 'open', 'closing', 'closed', 'archived']
TERMINAL_STATES = ['closed', 'archived']
ACTION_RULES = {'create': {'allowed_in_states': ['planned', 'open', 'closing'], 'transitions_to': None}, 'update': {'allowed_in_states': ['planned', 'open', 'closing'], 'transitions_to': None}, 'open': {'allowed_in_states': ['planned', 'open', 'closing'], 'transitions_to': None}, 'close': {'allowed_in_states': ['planned', 'open', 'closing'], 'transitions_to': 'closed'}, 'archive': {'allowed_in_states': ['planned', 'open', 'closing'], 'transitions_to': 'archived'}}

STATE_FIELD = 'workflow_state'
WORKFLOW_HINTS = {'business_objective': 'collect accounting records for a reporting period, generate financial statements, review them, and publish management-ready financial outputs', 'actors': ['finance controller', 'reporting accountant', 'approver', 'management audience'], 'start_condition': 'a reporting period is ready for statement preparation', 'ordered_steps': ['Confirm the reporting period and close readiness.'], 'primary_actions': ['review', 'approve', 'close'], 'primary_transitions': ['reporting_period: open -> closing -> closed'], 'downstream_effects': ['feeds management reporting, audit, compliance, and executive decision-making'], 'action_actors': {'create': ['finance controller'], 'update': ['finance controller'], 'close': ['finance controller'], 'archive': ['finance controller']}}

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
        return {'mode': 'configuration_control', 'case_management': False}

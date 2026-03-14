"""Workflow service seed for financial_statement_run."""

from __future__ import annotations


DOC_ID = "financial_statement_run"
ARCHETYPE = "transaction"
INITIAL_STATE = 'draft'
STATES = ['draft', 'generated', 'reviewed', 'approved', 'published', 'archived']
TERMINAL_STATES = ['archived']
ACTION_RULES = {'create': {'allowed_in_states': ['draft', 'generated', 'reviewed', 'approved', 'published'], 'transitions_to': None}, 'generate': {'allowed_in_states': ['draft', 'generated', 'reviewed', 'approved', 'published'], 'transitions_to': None}, 'review': {'allowed_in_states': ['draft', 'generated', 'reviewed', 'approved', 'published'], 'transitions_to': 'reviewed'}, 'approve': {'allowed_in_states': ['draft', 'generated', 'reviewed', 'approved', 'published'], 'transitions_to': 'approved'}, 'publish': {'allowed_in_states': ['draft', 'generated', 'reviewed', 'approved', 'published'], 'transitions_to': 'published'}, 'archive': {'allowed_in_states': ['draft', 'generated', 'reviewed', 'approved', 'published'], 'transitions_to': 'archived'}}

STATE_FIELD = 'workflow_state'
WORKFLOW_HINTS = {'business_objective': 'collect accounting records for a reporting period, generate financial statements, review them, and publish management-ready financial outputs', 'actors': ['finance controller', 'reporting accountant', 'approver', 'management audience'], 'start_condition': 'a reporting period is ready for statement preparation', 'ordered_steps': ['Create the statement generation run.', 'Review, approve, and publish the statement set.'], 'primary_actions': ['create', 'generate', 'review', 'approve', 'publish'], 'primary_transitions': ['financial_statement_run: draft -> generated', 'financial_statement_run: generated -> reviewed -> approved -> published'], 'downstream_effects': ['feeds management reporting, audit, compliance, and executive decision-making']}

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
        return {'mode': 'transaction_flow', 'supports_submission': True}

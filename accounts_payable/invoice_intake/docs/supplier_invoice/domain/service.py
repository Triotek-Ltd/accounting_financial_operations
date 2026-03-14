"""Business-domain service seed for Supplier Invoice."""

from __future__ import annotations


ARCHETYPE_PROFILE = {'workflow_profile': {'mode': 'transaction_flow', 'supports_submission': True}, 'reporting_profile': {'supports_snapshots': True, 'supports_outputs': True}, 'integration_profile': {'external_sync_enabled': True, 'tracks_external_refs': True}, 'lifecycle_states': ['draft', 'approved', 'payable', 'partially_paid', 'paid', 'archived'], 'is_transactional': True}

CONTRACT = {'title_field': 'title', 'status_field': 'workflow_state', 'reference_field': 'reference_no', 'required_fields': ['title', 'workflow_state', 'transaction_date'], 'field_purposes': {'workflow_state': 'lifecycle_state', 'transaction_date': 'transaction_date', 'party': 'primary_party', 'currency': 'currency_code', 'total_amount': 'total_amount', 'invoice_number': 'reference', 'supplier': 'party_reference', 'invoice_date': 'schedule_marker', 'due_date': 'schedule_marker', 'totals': 'structured_payload', 'approval_status': 'status_flag', 'payment_status': 'status_flag'}, 'search_fields': ['title', 'reference_no', 'description', 'invoice_number', 'supplier', 'invoice_date'], 'list_columns': ['title', 'reference_no', 'transaction_date', 'party', 'total_amount', 'workflow_state'], 'initial_state': 'draft', 'lifecycle_states': ['draft', 'approved', 'payable', 'partially_paid', 'paid', 'archived'], 'terminal_states': ['paid', 'archived'], 'action_targets': {'create': None, 'update': None, 'review': None, 'approve': 'approved', 'post': None, 'mark_payable': None, 'archive': 'archived'}}

WORKFLOW_HINTS = {'business_objective': 'receive supplier invoices, verify them against procurement evidence, approve them, pay them, and keep the payable ledger current', 'actors': ['AP clerk', 'reviewer', 'approver', 'treasury or finance officer'], 'start_condition': 'a supplier invoice is received', 'ordered_steps': ['Capture the supplier invoice and basic terms.', 'Match invoice against purchase and receipt records.', 'Reconcile payment against invoice balances.', 'Archive invoice and payment evidence.'], 'primary_actions': ['create', 'update', 'review', 'approve', 'reconcile', 'mark_payable', 'archive'], 'primary_transitions': ['supplier_invoice: draft', 'supplier_invoice: draft -> approved -> payable', 'supplier_invoice: payable -> partially_paid or paid'], 'downstream_effects': ['updates AP aging, cash management, bookkeeping, and supplier history']}

class DomainService:
    doc_id = "supplier_invoice"
    archetype = "transaction"
    doc_kind = "transaction"

    def required_fields(self) -> list[str]:
        return CONTRACT.get("required_fields", [])

    def state_field(self) -> str | None:
        return CONTRACT.get("status_field")

    def default_state(self) -> str | None:
        return CONTRACT.get("initial_state")

    def list_columns(self) -> list[str]:
        return CONTRACT.get("list_columns", [])

    def validate_invariants(self, payload: dict, *, partial: bool = False) -> dict:
        if partial:
            required_scope = [field for field in self.required_fields() if field in payload]
        else:
            required_scope = self.required_fields()
        missing_fields = [field for field in required_scope if not payload.get(field)]
        if missing_fields:
            raise ValueError(f"Missing required business fields: {', '.join(missing_fields)}")
        state_field = self.state_field()
        allowed_states = set(CONTRACT.get("lifecycle_states", []))
        if state_field and payload.get(state_field) and allowed_states and payload[state_field] not in allowed_states:
            raise ValueError(f"Invalid state '{payload[state_field]}' for {state_field}")
        return payload

    def prepare_create_payload(self, payload: dict, context: dict | None = None) -> dict:
        payload = dict(payload)
        state_field = self.state_field()
        if state_field and not payload.get(state_field) and self.default_state():
            payload[state_field] = self.default_state()
        title_field = CONTRACT.get("title_field")
        reference_field = CONTRACT.get("reference_field")
        if title_field and not payload.get(title_field) and reference_field and payload.get(reference_field):
            payload[title_field] = str(payload[reference_field])
        payload = self.validate_invariants(payload)
        return payload

    def after_create(self, instance, serialized_data: dict, context: dict | None = None) -> dict:
        return serialized_data

    def prepare_update_payload(self, instance, payload: dict, context: dict | None = None) -> dict:
        payload = dict(payload)
        payload = self.validate_invariants(payload, partial=True)
        return payload

    def after_update(self, instance, serialized_data: dict, context: dict | None = None) -> dict:
        return serialized_data

    def shape_retrieve_data(self, instance, serialized_data: dict, context: dict | None = None) -> dict:
        serialized_data.setdefault("_business_capabilities", self.business_capabilities())
        return serialized_data

    def workflow_objective(self) -> str | None:
        return WORKFLOW_HINTS.get("business_objective")

    def business_capabilities(self) -> dict:
        return {
            **ARCHETYPE_PROFILE,
            "required_fields": self.required_fields(),
            "state_field": self.state_field(),
            "default_state": self.default_state(),
        }

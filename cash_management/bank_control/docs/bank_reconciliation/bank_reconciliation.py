"""Doc runtime hooks for bank_reconciliation."""

class DocRuntime:
    doc_key = "bank_reconciliation"

    def validate(self, payload):
        return payload

    def allowed_actions(self):
        return ['create', 'match', 'review', 'approve', 'close', 'archive']

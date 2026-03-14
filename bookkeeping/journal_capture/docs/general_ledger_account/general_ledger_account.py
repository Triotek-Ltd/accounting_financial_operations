"""Doc runtime hooks for general_ledger_account."""

class DocRuntime:
    doc_key = "general_ledger_account"

    def validate(self, payload):
        return payload

    def allowed_actions(self):
        return ['create', 'update', 'review', 'archive']

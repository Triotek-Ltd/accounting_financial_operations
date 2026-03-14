"""Doc runtime hooks for cash_account."""

class DocRuntime:
    doc_key = "cash_account"

    def validate(self, payload):
        return payload

    def allowed_actions(self):
        return ['create', 'update', 'review', 'archive']

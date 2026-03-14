"""Doc runtime hooks for ledger_posting."""

class DocRuntime:
    doc_key = "ledger_posting"

    def validate(self, payload):
        return payload

    def allowed_actions(self):
        return ['record', 'review', 'reverse', 'archive']

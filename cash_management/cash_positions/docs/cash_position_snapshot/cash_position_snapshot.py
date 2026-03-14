"""Doc runtime hooks for cash_position_snapshot."""

class DocRuntime:
    doc_key = "cash_position_snapshot"

    def validate(self, payload):
        return payload

    def allowed_actions(self):
        return ['create', 'review', 'archive']

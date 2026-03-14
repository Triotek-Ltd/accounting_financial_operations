"""Doc runtime hooks for variance_record."""

class DocRuntime:
    doc_key = "variance_record"

    def validate(self, payload):
        return payload

    def allowed_actions(self):
        return ['record', 'review', 'escalate', 'archive']

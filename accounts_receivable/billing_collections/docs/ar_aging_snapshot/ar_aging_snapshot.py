"""Doc runtime hooks for ar_aging_snapshot."""

class DocRuntime:
    doc_key = "ar_aging_snapshot"

    def validate(self, payload):
        return payload

    def allowed_actions(self):
        return ['create', 'review', 'archive']

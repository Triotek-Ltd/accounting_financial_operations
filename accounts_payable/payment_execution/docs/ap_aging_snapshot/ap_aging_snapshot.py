"""Doc runtime hooks for ap_aging_snapshot."""

class DocRuntime:
    doc_key = "ap_aging_snapshot"

    def validate(self, payload):
        return payload

    def allowed_actions(self):
        return ['create', 'review', 'archive']

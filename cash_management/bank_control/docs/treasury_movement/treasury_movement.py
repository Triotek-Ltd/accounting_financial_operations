"""Doc runtime hooks for treasury_movement."""

class DocRuntime:
    doc_key = "treasury_movement"

    def validate(self, payload):
        return payload

    def allowed_actions(self):
        return ['create', 'review', 'approve', 'post', 'reverse', 'archive']

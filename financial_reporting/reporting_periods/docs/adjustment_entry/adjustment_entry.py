"""Doc runtime hooks for adjustment_entry."""

class DocRuntime:
    doc_key = "adjustment_entry"

    def validate(self, payload):
        return payload

    def allowed_actions(self):
        return ['create', 'review', 'approve', 'post', 'reverse', 'archive']

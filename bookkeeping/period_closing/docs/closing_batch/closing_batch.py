"""Doc runtime hooks for closing_batch."""

class DocRuntime:
    doc_key = "closing_batch"

    def validate(self, payload):
        return payload

    def allowed_actions(self):
        return ['create', 'assign', 'review', 'approve', 'close', 'reopen', 'archive']

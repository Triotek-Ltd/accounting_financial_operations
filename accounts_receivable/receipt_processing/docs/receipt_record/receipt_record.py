"""Doc runtime hooks for receipt_record."""

class DocRuntime:
    doc_key = "receipt_record"

    def validate(self, payload):
        return payload

    def allowed_actions(self):
        return ['create', 'review', 'approve', 'post', 'reconcile', 'reverse', 'archive']

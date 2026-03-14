"""Doc runtime hooks for payment_request."""

class DocRuntime:
    doc_key = "payment_request"

    def validate(self, payload):
        return payload

    def allowed_actions(self):
        return ['create', 'submit', 'review', 'approve', 'reject', 'execute', 'cancel', 'archive']

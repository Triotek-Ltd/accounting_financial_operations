"""Doc runtime hooks for customer_invoice."""

class DocRuntime:
    doc_key = "customer_invoice"

    def validate(self, payload):
        return payload

    def allowed_actions(self):
        return ['create', 'update', 'review', 'approve', 'post', 'issue', 'archive']

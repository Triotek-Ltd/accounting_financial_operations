"""Doc runtime hooks for supplier_payment."""

class DocRuntime:
    doc_key = "supplier_payment"

    def validate(self, payload):
        return payload

    def allowed_actions(self):
        return ['create', 'review', 'approve', 'post', 'reconcile', 'reverse', 'archive']

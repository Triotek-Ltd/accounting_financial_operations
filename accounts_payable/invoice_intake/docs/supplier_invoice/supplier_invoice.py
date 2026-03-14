"""Doc runtime hooks for supplier_invoice."""

class DocRuntime:
    doc_key = "supplier_invoice"

    def validate(self, payload):
        return payload

    def allowed_actions(self):
        return ['create', 'update', 'review', 'approve', 'post', 'mark_payable', 'archive']

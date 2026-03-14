"""Doc runtime hooks for cost_allocation_rule."""

class DocRuntime:
    doc_key = "cost_allocation_rule"

    def validate(self, payload):
        return payload

    def allowed_actions(self):
        return ['create', 'update', 'review', 'approve', 'archive']

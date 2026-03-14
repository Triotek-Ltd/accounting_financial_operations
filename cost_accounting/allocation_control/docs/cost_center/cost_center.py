"""Doc runtime hooks for cost_center."""

class DocRuntime:
    doc_key = "cost_center"

    def validate(self, payload):
        return payload

    def allowed_actions(self):
        return ['create', 'update', 'review', 'archive']

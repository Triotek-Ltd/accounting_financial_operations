"""Doc runtime hooks for cost_record."""

class DocRuntime:
    doc_key = "cost_record"

    def validate(self, payload):
        return payload

    def allowed_actions(self):
        return ['create', 'review', 'allocate', 'post', 'archive']

"""Doc runtime hooks for collection_case."""

class DocRuntime:
    doc_key = "collection_case"

    def validate(self, payload):
        return payload

    def allowed_actions(self):
        return ['create', 'assign', 'contact', 'escalate', 'resolve', 'close', 'archive']

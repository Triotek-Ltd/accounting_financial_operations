"""Doc runtime hooks for statement_line."""

class DocRuntime:
    doc_key = "statement_line"

    def validate(self, payload):
        return payload

    def allowed_actions(self):
        return ['record', 'review', 'archive']

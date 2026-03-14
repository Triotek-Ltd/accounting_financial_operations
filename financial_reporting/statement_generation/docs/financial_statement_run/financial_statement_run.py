"""Doc runtime hooks for financial_statement_run."""

class DocRuntime:
    doc_key = "financial_statement_run"

    def validate(self, payload):
        return payload

    def allowed_actions(self):
        return ['create', 'generate', 'review', 'approve', 'publish', 'archive']

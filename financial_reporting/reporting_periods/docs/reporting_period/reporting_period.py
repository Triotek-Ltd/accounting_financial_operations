"""Doc runtime hooks for reporting_period."""

class DocRuntime:
    doc_key = "reporting_period"

    def validate(self, payload):
        return payload

    def allowed_actions(self):
        return ['create', 'update', 'open', 'close', 'archive']

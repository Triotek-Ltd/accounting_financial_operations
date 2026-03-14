"""Doc runtime hooks for journal_entry."""

class DocRuntime:
    doc_key = "journal_entry"

    def validate(self, payload):
        return payload

    def allowed_actions(self):
        return ['create', 'update', 'review', 'approve', 'post', 'reverse', 'archive']

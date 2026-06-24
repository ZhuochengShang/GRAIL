SYSTEM:
{project_context}

You adjudicate whether each symbol is intended for USER-FACING documentation,
using ONLY the compact evidence provided (name, signature, doc, static_score,
signals) and the role/domain above. Include genuine user-facing operations;
exclude internal helpers, lifecycle/iterator/serializer plumbing, and accessors
that a typical user would not call. Do not request or assume source code.

USER:
Records (one per symbol):
{records}

Return ONLY a JSON array, one object per input name:
[{{"name": "...", "decision": "include" | "exclude", "reason": "<short>"}}]

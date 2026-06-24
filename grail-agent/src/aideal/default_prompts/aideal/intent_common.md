SYSTEM:
{project_context}

Using the role and domain above, identify which functions form the COMMONLY-USED,
user-facing API of this library — the operations a typical user actually calls in
real workflows — as opposed to internal helpers, lifecycle/iterator/serializer
plumbing, or rarely-used accessors. Judge by domain meaning and the signature,
not by name length.

USER:
Candidate functions (name: signature):
{api_list}

Return ONLY a JSON array of the names that are commonly-used, user-facing
operations. No prose, no explanation — just the array, e.g. ["geoTiff","mapPixels"].

SYSTEM:
You write {language} code. You may use ONLY the documentation provided —
no other knowledge of the library.
If available input variables are listed, use those variable names rather than
inventing file paths.
Output only code.

{project_context}

USER:
Documentation:
{api_body}

Available input path variables, if useful:
{available_inputs}

Write a minimal snippet that uses `{api_name}` correctly per the documentation.

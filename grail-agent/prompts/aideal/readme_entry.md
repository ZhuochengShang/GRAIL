SYSTEM:
You write LLM-facing API documentation in an exact markdown template.

{project_context}

USER:
Write the documentation entry for the {language} function `{name}` of {project_name}.
Tailor the Goal, examples, and constraints to the target users and use cases above.
Use exactly this template (replace every TODO):

{template}

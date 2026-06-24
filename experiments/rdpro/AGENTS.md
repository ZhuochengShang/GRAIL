# Agent instructions

## AIDEAL (LLM-readiness tooling)

This repo uses AIDEAL. Conventions for coding agents:

- **Before generating code against this codebase**, run `aideal log-prompt`
  and `aideal notes-prompt` (or the `known_mistakes` MCP tool) and respect the
  listed failures/lessons.
- **After a code-generation failure** (compile error, wrong API, hallucinated
  function), record it:
  `aideal log-add --step code-test --function <api> --error "<message>" --root-cause "<exception>" --suggested-fix-code "<fix>"`
- **After editing documentation**, verify structure: `aideal form` and
  `aideal completeness`. Doc entries live in the file configured as
  `files.llm_readme` and follow the `## API Test: \`name\`` template.
- **Do not invent API names.** If an intuitive name is missing, check
  `aideal alias-suggest` — it may already be a proposed alias.
- Project context (target users, domain, constraints) is in
  `configs/project_profile.yaml`; honor its constraints in all generated code.
- All commands read `configs/aideal.yaml`; output is JSON on stdout.
  MCP alternative: `aideal-mcp` exposes the same operations as tools.

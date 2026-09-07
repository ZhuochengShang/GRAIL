# Experiment data and API-test verification

This checks pinned input identity and records test evidence. It does not certify every generated assertion or API/data pairing.

| Repository | Cell | Input provenance check | Issues |
|---|---|---|---|
| mir_eval | A1 | PASS_WITH_LIMITATIONS | supplied output directory does not currently exist; write APIs may fail before the target call |
| mir_eval | A2 | PASS_WITH_LIMITATIONS | supplied output directory does not currently exist; write APIs may fail before the target call |
| mir_eval | B1 | pending | none observed |
| mir_eval | B2 | pending | none observed |
| thumbnailator | A1 | PASS_WITH_LIMITATIONS | none observed |
| thumbnailator | A2 | PASS_WITH_LIMITATIONS | none observed |
| thumbnailator | B1 | pending | none observed |
| thumbnailator | B2 | pending | none observed |
| tslearn | A1 | PASS_WITH_LIMITATIONS | none observed |
| tslearn | A2 | PASS_WITH_LIMITATIONS | supplied output directory does not currently exist; write APIs may fail before the target call |
| tslearn | B1 | pending | none observed |
| tslearn | B2 | pending | none observed |

For each active cell, data_evidence.json lists absolute input paths, SHA-256, pinned Git blobs, decoded file metadata, manifest/config/profile/scaffold hashes, and completed-result consistency checks. api_test_data.csv covers every manifest API and records which supplied fixtures or preloaded values are referenced inside its generated snippet, plus target-call/assertion/witness text. Textual references are evidence for review, not proof of runtime dataflow or semantic correctness.

Inputs are checked against pinned source blobs; generated outputs are recorded separately. Do not install dependencies, alter fixture contents, or fix assertions inside active measured conditions. Use separate diagnostic copies and retain native scores.

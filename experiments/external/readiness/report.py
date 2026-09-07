"""Read existing ledgers and render the central readiness report and cards."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from experiments.external.audit_overnight import atomic, dump
from experiments.external.readiness.model import assess, suggestion
from experiments.external.readiness.review import history, state


def load(path, default=None):
    if not path.exists() and default is not None:
        return default, None
    raw = path.read_bytes()
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def collect(report, repositories=None):
    releases, _ = load(report/'data_validation/release_status.json')
    names = repositories or sorted(releases)
    assessments, cards, errors = {}, [], []
    for repo in names:
        if Path(repo).name != repo or repo in ('.', '..'):
            raise ValueError('Repository must be a single directory name')
        assessments[repo] = {'comparison_release': releases.get(repo, 'unverified'), 'cells': {}}
        for cell in ('A1', 'A2', 'B1', 'B2'):
            try:
                ledger_path = report/repo/cell/'ledger.json'
                ledger, checksum = load(ledger_path)
                data, _ = load(report/'data_validation'/repo/cell/'data_evidence.json', {})
                config, _ = load(report/'data_validation/automation'/repo/cell/'config_bundle.json', {})
                assessment = assess(ledger, data, config)
                assessment['provenance'] = {'ledger': f'{repo}/{cell}/ledger.json', 'sha256': checksum,
                    'source_commit': data.get('upstream_commit'), 'manifest_sha256': ledger.get('manifest_file_sha256'),
                    'effective_config_sha256': config.get('effective_config_sha256')}
                assessments[repo]['cells'][cell] = assessment
                input_rows = {r['api']: r for r in data.get('api_test_evidence', [])}
                for row in ledger['rows']:
                    if row.get('status') == 'fail':
                        card = suggestion(repo, cell, row, ledger, input_rows.get(row['api']))
                        card['evidence_ledger'] = f'{repo}/{cell}/ledger.json'
                        card['evidence_ledger_sha256'] = checksum
                        cards.append(card)
            except (OSError, ValueError, KeyError, TypeError) as exc:
                errors.append(f'{repo}/{cell}: {type(exc).__name__}: {exc}')
    return assessments, cards, errors


def cell_text(cell):
    if not cell:
        return 'evidence unavailable'
    if cell['counts'].get('pending') == cell['denominator']:
        return f"pending ({cell['denominator']} APIs)"
    value = f"{cell['provisional_passes']}/{cell['denominator']}"
    return value + (' final' if cell['status'] == 'complete_measurement' else ' provisional')


def card_markdown(card):
    review = card['review']
    lines = [f"# {card['title']}", '',
             f"ID: `{card['id']}` · {card['repository']}/{card['cell']} · **{review['status']}**", '',
             f"Evidence version: `{card['evidence_version']}`", '',
             f"Candidate category: **{card['candidate_category']}**. Confidence: **{card['confidence']}**.", '',
             '## Barrier and evidence', '', str(card['diagnosis']), '',
             f"Source: `{card['evidence'].get('source')}`. Native category: `{card['evidence'].get('native_category')}`.", '',
             '```text', str(card['evidence'].get('error') or '').replace('```', "'''"), '```', '',
             f"[Evidence ledger](../../../{card['evidence_ledger']}) · [Saved evidence](../evidence/{card['evidence_version']}.json)", '',
             f"Recorded attempts: {card['attempts']}; provider errors: {card['provider_error_attempts']}; document rounds: {card['document_rounds']}.", '',
             '## Proposed action', '', card['proposed_action'], '',
             '## Required validation', '', card['validation_criteria'], '',
             card['expected_benefit'], '',
             '## Review and implementation', '',
             'Choose a concrete plan, then assign approved work to a human or agent. This card never executes changes.', '',
             'Reviewer acceptance does not alter measured scores or certify readiness. New improvements need matched evaluation evidence.', '',
             '```json', json.dumps(review, indent=2, ensure_ascii=False).replace('```', "'''"), '```', '']
    return '\n'.join(lines)


def publish(report, repositories=None):
    out = report/'data_validation/readiness'
    out.mkdir(parents=True, exist_ok=True)
    assessments, cards, errors = collect(report, repositories)
    events = history(out/'decisions.jsonl')
    cards.sort(key=lambda c: ({'execution_blocker': 0, 'reviewed_barrier': 1, 'needs_diagnosis': 2}[c['priority']], c['repository'], c['cell'], c['api']))
    active_ids = {c['id'] for c in cards}
    archived = sorted({e['id'] for e in events}-active_ids)
    for card in cards:
        card['review'] = state(card, events)
        evidence = out/'evidence'/f"{card['evidence_version']}.json"
        if not evidence.exists():
            dump(evidence, card['evidence'])
        atomic(out/'suggestions'/f"{card['id']}.md", card_markdown(card))
    assessment = {'schema_version': 1, 'generated_at': datetime.now(timezone.utc).isoformat(),
                  'repositories': assessments, 'errors': errors,
                  'overall_score': None, 'limitations': [
                      'Documentation-conditioned API execution is the current measured capability.',
                      'Discovery, autonomous installation, held-out workflows and recovery are not fully measured.',
                      'A native passing test is not independent proof of correct inputs or assertions.']}
    queue = {'schema_version': 1, 'cards': cards, 'inactive_reviewed_ids': archived,
             'inactive_meaning': 'No current failure card; absence is not proof that an accepted improvement caused recovery.',
             'decision_log': 'decisions.jsonl'}
    dump(out/'assessment.json', assessment)
    dump(out/'improvement_queue.json', queue)
    counts = Counter(c['review']['status'] for c in cards)
    barriers = Counter((c['repository'], c['candidate_category']) for c in cards)
    lines = ['# AIDEAL readiness assessment and improvement queue', '',
             f"Updated: {assessment['generated_at']}", '',
             '**Measured scope:** how documentation affects an LLM’s API use under a fixed harness. Overall agent readiness is not yet fully measured; no composite score is assigned.', '',
             '| Repository | A1 | A2 | B1 | B2 | Matched comparison |', '|---|---|---|---|---|---|']
    for repo, summary in assessments.items():
        lines.append('| ' + ' | '.join([repo, *(cell_text(summary['cells'].get(c)) for c in ('A1','A2','B1','B2')), summary['comparison_release']]) + ' |')
    lines += ['', 'Provisional counts retain pending and provider-error APIs in the denominator. Final counts are native pass/all-API results. Cross-cell effects require the separate matched-comparison release checks.', '',
              '| Readiness dimension | Current evidence |', '|---|---|',
              '| Discovery | Not measured: the target API is supplied. |',
              '| Setup and inputs | Partial: frozen configuration and fixture identity; autonomous setup and API-specific suitability remain unverified. |',
              '| API execution | Measured in complete cells; provisional elsewhere. |',
              '| Workflow completion | Not measured: held-out multi-API tasks are needed. |',
              '| Verification and recovery | Partial: assertions and retry histories; independent oracle checks and agent recovery tasks are needed. |', '',
              '## Observed barriers', '',
              '| Repository | Candidate barrier | Affected API/cell records |', '|---|---|---:|']
    lines += [f'| {repo} | {category} | {count} |' for (repo, category), count in sorted(barriers.items())]
    lines += ['', f"## Reviewable improvements ({len(cards)})", '',
              f"Review states: `{dict(counts)}`. Observation errors: {len(errors)}. Inactive reviewed IDs retained: {len(archived)}.", '',
              'Each card separates native failure, diagnosis confidence, proposed action, validation and review decisions. Provider barriers concern execution infrastructure; they are not automatically codebase or documentation defects.', '',
              '| Suggestion | Cell | Priority | Confidence | Review |', '|---|---|---|---|---|']
    for card in cards:
        lines.append(f"| [{card['repository']}: {card['api']}](suggestions/{card['id']}.md) | {card['cell']} | {card['priority']} | {card['confidence']} | {card['review']['status']} |")
    lines += ['', '## Human and agent workflow', '',
              '`open → proposed → human-approved plan → human/agent implementation → submitted validation → human acceptance or revision`', '',
              'Defer or reject any suggestion. A changed evidence version makes older decisions stale. Actor labels are operator-supplied audit records, not an authentication system. Approval records authorize no automatic subprocess or LLM execution in this tool.', '',
              '- [Review command and decision formats](WORKFLOW.md)',
              '- [Machine-readable assessment](assessment.json) · [Improvement queue](improvement_queue.json)',
              '- [Architecture and human involvement](../AIDEAL_DESIGN_LOGIC.md)',
              '- [Data, formats, samples, and API tests](../FINAL_REPORT_DATA_AND_API_METHODS.md)',
              '- [Detailed 2×2 evidence](../../DETAILED_PRIORITY_REPORT.md)', '',
              'Errors: ' + ('; '.join(errors) if errors else 'none observed'), '']
    text = '\n'.join(lines)
    atomic(out/'ASSESSMENT.md', text)
    # A unique entry point; existing observers never write this filename.
    atomic(report/'AIDEAL_REPORT.md', '# AIDEAL central output\n\n'
           '[Open the readiness assessment and reviewable improvement queue](data_validation/readiness/ASSESSMENT.md).\n\n'
           'This report separates measured API usability from unmeasured readiness dimensions and preserves native experiment outcomes.\n')
    return assessment, queue

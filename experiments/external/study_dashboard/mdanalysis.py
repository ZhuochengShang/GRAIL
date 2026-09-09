"""Read MDAnalysis's new isolated continuation without inventing measurements."""
import json


def current(parent, evidence):
    out = parent / 'AIDEAL_mdanalysis_v4'
    registration = out / 'registration.json'
    legacy = parent / 'GRAIL_rdpro_puzzle_aideal/experiments/external/mdanalysis_pipeline_watchdog.state.json'
    info = {'legacy': evidence.json(legacy), 'registration': None, 'jobs': {}, 'generation': None}
    cells = []
    if registration.exists():
        info['registration'] = evidence.json(registration)
        state = out / 'study_watchdog.state.json'
        if state.exists():
            info['jobs'] = evidence.json(state).get('jobs', {})
        for cell, item in info['registration']['cells'].items():
            root = parent / item['root']
            result = root / f'docs/full_1032/{cell}/comprehension.json'
            checkpoint = root / f'.aideal_exec/full_1032/{cell}/comprehension_progress.jsonl'
            metrics = {}
            if result.exists():
                metrics = evidence.json(result).get('metrics', {})
            elif checkpoint.exists():
                rows = []
                lines = evidence.text(checkpoint).splitlines()
                for i, line in enumerate(lines):
                    try:
                        rows.append(json.loads(line))
                    except ValueError:
                        if i != len(lines)-1:
                            raise
                fingerprints = {r.get('experiment_fingerprint') for r in rows}
                if len(fingerprints) > 1:
                    raise ValueError('MDAnalysis checkpoint contains mixed experiment identities')
                metrics = {r['name']: r for r in rows}
            cells.append({'cell': cell, 'expected': 1032, 'recorded': len(metrics),
                'pass': sum(r.get('status')=='pass' for r in metrics.values()) if metrics else None,
                'state': info['jobs'].get(f'{cell}_zero', {}).get('status', 'prepared; not admitted')})
            if cell == 'A2':
                gen = root / '.aideal_exec/readme_generation_state.json'
                if gen.exists():
                    raw = evidence.json(gen)
                    info['generation'] = {k: raw.get(k) for k in ('completed_count', 'target_count', 'complete')}
    else:
        cells = [{'cell': c, 'expected': 1032, 'recorded': 0, 'pass': None,
                  'state': 'No measured outcomes; runtime preflight in progress'} for c in ('A1', 'A2', 'B2')]
    baseline = parent / 'GRAIL_mdanalysis_full1032_freeze/experiments/mdanalysis/docs/full_1032/setup/PASS_TO_PASS_BEFORE.json'
    if baseline.exists():
        raw = evidence.json(baseline)
        info['upstream'] = {k: raw.get(k) for k in ('passed', 'counts', 'case_count', 'wall_s')}
    else:
        info['upstream'] = {'state': 'Existing local upstream preflight started; no final result yet'}
    return cells, info

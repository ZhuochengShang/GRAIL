"""Offline next-protocol input contracts and conservative Python test lint.

No generated code is executed. A passing metadata contract is not a semantic
certificate. Intended for a frozen next protocol, not retroactive rescoring.
"""
import ast


def validate_inputs(contract, observed):
    """Compare supplied metadata with explicit requirements; fail closed."""
    issues = []
    if contract.get('schema_version') != 1 or not isinstance(contract.get('api'), str) or not contract['api']:
        return {'status': 'invalid_contract', 'issues': ['schema_version=1 and a canonical api are required']}
    required = contract.get('inputs')
    if not isinstance(required, dict):
        return {'status': 'invalid_contract', 'issues': ['inputs must be an object (empty only for an explicitly input-free API)']}
    allowed = {'shape', 'dtype', 'units', 'format', 'columns', 'exists'}
    for name, rules in required.items():
        if not isinstance(rules, dict) or set(rules)-allowed:
            issues.append(f'{name}: unsupported or malformed constraints')
            continue
        if name not in observed:
            issues.append(f'{name}: missing observed input metadata')
            continue
        actual = observed[name]
        for key, expected in rules.items():
            if key not in actual:
                issues.append(f'{name}.{key}: unobserved')
            elif key == 'shape':
                shape = actual[key]
                if not isinstance(expected, list) or not isinstance(shape, list) or len(expected) != len(shape) or any(
                        wanted is not None and wanted != got for wanted, got in zip(expected, shape)):
                    issues.append(f'{name}.shape: expected {expected}, observed {shape}')
            elif actual[key] != expected:
                issues.append(f'{name}.{key}: expected {expected!r}, observed {actual[key]!r}')
    return {'status': 'mismatch' if issues else 'metadata_matches', 'issues': issues,
            'semantic_validation': 'not established', 'api': contract.get('api')}


def lint_python(code, target):
    """Collect AST evidence; aliases/reassignments/dynamic calls need review."""
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return {'status': 'syntax_error', 'error': str(exc), 'semantic_validation': 'unverified'}
    aliases = {}
    assigned = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                aliases[alias.asname or alias.name.split('.')[0]] = alias.name if alias.asname else alias.name.split('.')[0]
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            for alias in node.names:
                aliases[alias.asname or alias.name] = node.module + '.' + alias.name
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            assigned.add(node.id)
        elif isinstance(node, ast.arg):
            assigned.add(node.arg)
    def dotted(node):
        if isinstance(node, ast.Name):
            return None if node.id in assigned else aliases.get(node.id, node.id)
        if isinstance(node, ast.Attribute):
            base = dotted(node.value)
            return base + '.' + node.attr if base else None
        return None
    calls = [{'line': n.lineno, 'call': ast.unparse(n)} for n in ast.walk(tree)
             if isinstance(n, ast.Call) and dotted(n.func) == target]
    assertions = [n for n in ast.walk(tree) if isinstance(n, ast.Assert)]
    trivial = [n.lineno for n in assertions if isinstance(n.test, ast.Constant) or (
        isinstance(n.test, ast.Compare) and len(n.test.comparators) == 1 and
        isinstance(n.test.ops[0], (ast.Eq, ast.Is)) and
        ast.dump(n.test.left) == ast.dump(n.test.comparators[0]))]
    return {'status': 'review_required', 'target': target, 'candidate_calls': calls,
            'assertion_lines': [n.lineno for n in assertions], 'trivial_assertion_lines': trivial,
            'issues': ([] if calls else ['no statically resolved target call']) +
                      ([] if assertions else ['no Python assert statement']) +
                      ([] if not trivial else ['constant/self-equality assertion requires review']),
            'semantic_validation': 'unverified: AST presence does not prove execution, dataflow, or oracle validity'}

"""Deterministic local input/output checks; never repair generated code."""
from pathlib import Path
import hashlib


def prepare(project, input_files, output_directory):
    project=Path(project).resolve()
    output=Path(output_directory).resolve()
    if not output.is_relative_to(project / '.aideal_exec'):
        raise ValueError('Output must belong to this project execution directory')
    checked={}
    for name,relative in input_files.items():
        path=(project/relative).resolve()
        if not path.is_relative_to(project) or not path.is_file():
            raise ValueError(f'Configured input {name} is missing or outside project')
        checked[name]={'path':str(path),'kind':'input_file',
                       'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    # Only scaffold-owned output setup; do not touch fixtures or generated snippets.
    output.mkdir(parents=True,exist_ok=True)
    checked['output_dir']={'path':str(output),'kind':'output_directory','exists':output.is_dir()}
    return checked


def guidance(bindings):
    """Explicit binding text for a NEW matched prompt version, not frozen runs."""
    return '\n'.join(f"- {name}: {item['kind']}; exact path={item['path']}"
                     for name,item in bindings.items()) + (
        '\nUse input_file paths exactly; do not guess sibling fixtures. '
        'Create child output files only under output_directory. '
        'An output_file is already a filename: do not append child paths to it. '
        'If no supplied input matches the API contract, report that limitation; do not invent a path.')

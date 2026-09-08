from pathlib import Path
import pytest
from .input_contract import prepare, guidance


def test_missing_fixture_stops_before_output_creation(tmp_path):
    output=tmp_path/'.aideal_exec/case/output'
    with pytest.raises(ValueError,match='missing'):
        prepare(tmp_path,{'image':'missing.png'},output)
    assert not output.exists()


def test_output_created_inputs_unchanged_and_guidance_explicit(tmp_path):
    fixture=tmp_path/'fixture.txt';fixture.write_text('original')
    output=tmp_path/'.aideal_exec/A1/output'
    bindings=prepare(tmp_path,{'fixture':'fixture.txt'},output)
    assert output.is_dir() and fixture.read_text()=='original'
    assert bindings['fixture']['kind']=='input_file'
    assert 'output_directory' in guidance(bindings)
    assert 'do not guess sibling fixtures' in guidance(bindings)


def test_refuses_cross_condition_external_output(tmp_path):
    with pytest.raises(ValueError,match='Output'):
        prepare(tmp_path,{},tmp_path.parent/'other/output')


def test_file_is_not_silently_converted_to_directory(tmp_path):
    output=tmp_path/'.aideal_exec/A1/output';output.parent.mkdir(parents=True);output.write_text('existing')
    with pytest.raises(FileExistsError):prepare(tmp_path,{},output)
    assert output.read_text()=='existing'

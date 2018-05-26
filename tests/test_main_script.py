from subprocess import Popen, PIPE
import os
import json
from pytest import fixture

script = ["genderbias"]
examples = [dict(file="example_letters/letterofRecM", output_lines=6),
            dict(file="example_letters/letterofRecW", output_lines=10)]

@fixture(params = examples)
def example(request):
    return request.param

@fixture(params = ["-f", "--file"])
def file_flag(request):
    return request.param

@fixture(params = ["--json", "-j"])
def json_flag(request):
    return request.param

@fixture(params = ["--list-detectors"])
def list_detectors_flag(request):
    return request.param


def output_with_options(options, feed_in=""):
    popen = Popen(script + options, stdin=PIPE, stdout=PIPE, universal_newlines=True)
    return popen.communicate(feed_in)[0]


def test_meta_ensure_examples_exist(example):
    assert os.path.isfile(example['file'])

def test_script_help():
    start_help_text = 'usage: genderbias [-h]'
    assert start_help_text in output_with_options(["-h"])

def test_script_can_list_detectors(list_detectors_flag):
    output = output_with_options([list_detectors_flag])
    import os
    dirs = [os.path.join("genderbias",_dir) for _dir in os.listdir("genderbias")
            if _dir != "__pycache__" and os.path.isdir(os.path.join("genderbias", _dir))]
    assert output.strip().split("\n")[0] == "AVAILABLE DETECTORS:"
    assert len(output.strip().split("\n")) == len(dirs) + 1  # 1 from Header line

def test_script_file_flags(example, file_flag):
    output = output_with_options([file_flag, example['file']])
    assert len(output.strip().split("\n")) == example['output_lines']

def test_script_input_from_stdin(example):
    with open(example['file']) as stream:
        text = stream.read()
    output = output_with_options([], feed_in=text)
    assert len(output.strip().split("\n")) == example['output_lines']

def test_script_json_output(example, file_flag, json_flag):
    output = output_with_options([file_flag, example['file'], json_flag])
    data = json.loads(output.strip())
    assert isinstance(data, list)
    for element in data:
        assert isinstance(element, dict)
        for key in ('name', 'summary', 'flags'):
            assert key in element
        assert isinstance(element['name'], str)
        assert isinstance(element['summary'], str)
        assert isinstance(element['flags'], list)

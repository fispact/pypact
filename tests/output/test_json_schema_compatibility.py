import os
import pytest
import json
from jsonschema import validate, ValidationError
import pypact as pp
from pypact.filerecord import InventoryFileRecord as FileRecord


from tests.testerbase import REFERENCE_DIR

ROOT_DIR = os.path.dirname(REFERENCE_DIR)
schema_file = os.path.join(ROOT_DIR, 'schema.json')

with open(schema_file) as fid:
    schema = json.loads(fid.read())


@pytest.mark.parametrize("fispact_out_file_name", [
    'test31.out',
    'test91.out',
    'test121.out',
    'test127.out',
    'test_dpa.out',
])
def test_output_writes_correct_json(fispact_out_file_name):
    data_file_name = os.path.join(REFERENCE_DIR, fispact_out_file_name)
    filerecord = FileRecord(data_file_name)
    output = pp.Output()
    output.fispact_deserialize(filerecord)
    json_text = output.json_serialize()
    json_obj = json.loads(json_text)
    try:
        validate(json_obj, schema)
    except ValidationError:
        pytest.fail("File " + fispact_out_file_name + " is not compatible to schema.json", False)

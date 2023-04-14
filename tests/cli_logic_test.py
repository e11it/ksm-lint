import pytest
from .mock_data import MOCK_DATA
from csv import DictReader
from io import StringIO

from pydantic_common_models.ksm.csv_acl import KafkaACLCSV


def test_mock_acl():
    result = list()
    mock_data_csv_reader = DictReader(StringIO(MOCK_DATA))
    mock_data_csv_reader.fieldnames
    for line in mock_data_csv_reader:
        acl = KafkaACLCSV.from_orm(line)
        acl.resource_type.validate_operation(acl.operation)
        result.append(acl)

    assert len(result) == 9
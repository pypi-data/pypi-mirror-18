from datetime import datetime

import pytest

from ct_core_api.api.common import json_utils as ju
from ct_core_api.common import datetime_utils as du


TEST_DATETIME_NO_TZINFO_VALUE = datetime(2016, 06, 06, 12, 12)
TEST_DATETIME_NO_TZINFO_VALUE.replace(tzinfo=None)

TEST_DATETIME_NO_TIME_OR_TZINFO_VALUE = datetime(2016, 06, 06, 0, 0)
TEST_DATETIME_NO_TIME_OR_TZINFO_VALUE.replace(tzinfo=None)

TEST_DATETIME_UTC_TZINFO_VALUE = datetime(2016, 06, 06, 12, 12)
TEST_DATETIME_UTC_TZINFO_VALUE.replace(tzinfo=du.TimeZone.UTC)


@pytest.mark.parametrize('python_input,expected_json_output', [
    (TEST_DATETIME_NO_TZINFO_VALUE, '2016-06-06T12:12:00Z'),
    (TEST_DATETIME_NO_TIME_OR_TZINFO_VALUE, '2016-06-06T00:00:00Z'),
    (TEST_DATETIME_UTC_TZINFO_VALUE, '2016-06-06T12:12:00Z')])
def test_isoformat_serialization(python_input, expected_json_output):
    actual_json_output = ju.isoformat(python_input)
    assert expected_json_output == actual_json_output


@pytest.mark.parametrize('json_input,expected_python_output', [
    ('2016-06-06T12:12:00Z+00:00', TEST_DATETIME_NO_TZINFO_VALUE),
    ('2016-06-06T12:12:00Z', TEST_DATETIME_NO_TZINFO_VALUE),
    ('2016-06-06T12:12:00', TEST_DATETIME_NO_TZINFO_VALUE),

    ('2016-06-06T12:12:00Z+00:00', TEST_DATETIME_UTC_TZINFO_VALUE),
    ('2016-06-06T12:12:00Z', TEST_DATETIME_UTC_TZINFO_VALUE),
    ('2016-06-06T12:12:00', TEST_DATETIME_UTC_TZINFO_VALUE),

    ('2016-06-06', TEST_DATETIME_NO_TIME_OR_TZINFO_VALUE)])
def test_from_iso_deserialization(json_input, expected_python_output):
    actual_python_output = ju.from_iso(json_input)
    assert expected_python_output == actual_python_output


@pytest.mark.parametrize('json_input', [
    '2016-06-06X12:12:00Z+00:00',
    '2016-06-06T12:12:00Z+00:'])
def test_from_iso_deserialization_type_error(json_input):
    with pytest.raises(ValueError):
        ju.from_iso(json_input)


@pytest.mark.parametrize('json_input', [
    '2016-99-99',
    '2016-06-06T12:99:00Z+00:00'])
def test_from_iso_deserialization_value_error(json_input):
    with pytest.raises(ValueError):
        ju.from_iso(json_input)

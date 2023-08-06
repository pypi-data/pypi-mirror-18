from datetime import datetime, timedelta

from ct_core_api.api.core.schema import APISchema, ma


class DateTimeSchema(APISchema):
    datetime = ma.DateTime()
    time = ma.Time()
    time_delta = ma.TimeDelta()


def test_schema_dump_with_datetime_fields():
    dt = datetime(2016, 11, 29, 20, 55, 17, 365555)
    td = timedelta(hours=1, minutes=30)

    dts = DateTimeSchema()
    result = dts.dump(dict(datetime=dt, time=dt.time(), time_delta=td)).data

    assert result['datetime'] == '2016-11-29T20:55:17.365555Z'
    assert result['time'] == '20:55:17.365555'
    assert result['time_delta'] == int(td.total_seconds())  # 90 * 60 = 5400


def test_schema_load_with_datetime_fields():
    dt = datetime(2016, 11, 29, 20, 55, 17, 365555)
    td = timedelta(hours=1, minutes=30)

    dts = DateTimeSchema()
    result = dts.load(dict(
        datetime='2016-11-29T20:55:17.365555+00:00',
        time='20:55:17.365555',
        time_delta=int(td.total_seconds()))).data

    assert result['datetime'] == dt
    assert result['time'] == dt.time()
    assert result['time_delta'] == td

import imp
import yaml
import datetime
import pytz
from freezegun import freeze_time

reds = imp.load_source('reds', './lambda/reds.py')
a = reds.reds()

#details
unsupported_multi_az_available = {
        "MultiAZ": True,
        "DBInstanceStatus": "available",
        "DBInstanceClass": "db.r3.large",
    }
micro_single_az_available = {
        "MultiAZ": False,
        "DBInstanceStatus": "available",
        "DBInstanceClass": "db.t2.micro",
    }
micro_multi_az_available = {
        "MultiAZ": True,
        "DBInstanceStatus": "available",
        "DBInstanceClass": "db.t2.micro",
    }
micro_multi_az_modifying = {
        "MultiAZ": True,
        "DBInstanceStatus": "modifying",
        "DBInstanceClass": "db.t2.micro",
    }
medium_multi_az_available = {
        "MultiAZ": True,
        "DBInstanceStatus": "available",
        "DBInstanceClass": "db.m3.medium",
    }
#alarm_status
high_cpu = {
    "MetricAlarms": [{
        "AlarmDescription": "CPU High Alarm",
        "StateValue": "ALARM",
    }, {
        "AlarmDescription": "CPU Low Alarm",
        "StateValue": "OK",
    }, {
        "AlarmDescription": "CPU Credits Exhausted Alarm",
        "StateValue": "OK",
    }]
}
low_cpu = {
    "MetricAlarms": [{
        "AlarmDescription": "CPU High Alarm",
        "StateValue": "OK",
    }, {
        "AlarmDescription": "CPU Low Alarm",
        "StateValue": "ALARM",
    }, {
        "AlarmDescription": "CPU Credits Exhausted Alarm",
        "StateValue": "OK",
    }]
}
credits_low = {
    "MetricAlarms": [{
        "AlarmDescription": "CPU High Alarm",
        "StateValue": "OK",
    }, {
        "AlarmDescription": "CPU Low Alarm",
        "StateValue": "OK",
    }, {
        "AlarmDescription": "CPU Credits Exhausted Alarm",
        "StateValue": "ALARM",
    }]
}
high_cpu_credits_low = {
    "MetricAlarms": [{
        "AlarmDescription": "CPU High Alarm",
        "StateValue": "ALARM",
    }, {
        "AlarmDescription": "CPU Low Alarm",
        "StateValue": "OK",
    }, {
        "AlarmDescription": "CPU Credits Exhausted Alarm",
        "StateValue": "ALARM",
    }]
}
no_alarm = {
    "MetricAlarms": [{
        "AlarmDescription": "CPU High Alarm",
        "StateValue": "OK",
    }, {
        "AlarmDescription": "CPU Low Alarm",
        "StateValue": "OK",
    }, {
        "AlarmDescription": "CPU Credits Exhausted Alarm",
        "StateValue": "OK",
    }]
}
#events
friday_midday_update = {
    "Events": [{
        "Date": datetime.datetime(2016, 1, 1, 18, 0, 0, 0, tzinfo=pytz.utc),
        "Message": "Applying modification to database instance class",
        "SourceIdentifier": "mixhop-rds-master",
        "EventCategories": ["configuration change"],
        "SourceType": "db-instance"
    },
    {
        "Date": datetime.datetime(2016, 1, 1, 18, 30, 0, 0, tzinfo=pytz.utc),
        "Message": "Finished applying modification to DB instance class",
        "SourceIdentifier": "mixhop-rds-master",
        "EventCategories": ["configuration change"],
        "SourceType": "db-instance"
    }]
}
saturday_midday_update = {
    "Events": [{
        "Date": datetime.datetime(2016, 1, 2, 18, 0, 0, 0, tzinfo=pytz.utc),
        "Message": "Applying modification to database instance class",
        "SourceIdentifier": "mixhop-rds-master",
        "EventCategories": ["configuration change"],
        "SourceType": "db-instance"
    },
    {
        "Date": datetime.datetime(2016, 1, 2, 18, 30, 0, 0, tzinfo=pytz.utc),
        "Message": "Finished applying modification to DB instance class",
        "SourceIdentifier": "mixhop-rds-master",
        "EventCategories": ["configuration change"],
        "SourceType": "db-instance"
    }]
}
no_update = {
    "Events": []
}

def get_vars(extra=None):
    suffix = extra if extra else ""
    return [yaml.load(file("./tests/test_vars{}.yaml".format(suffix))),yaml.load(file('./tests/test_alarms.yaml'))]

@freeze_time("2016-01-01 19:30:00", tz_offset=0)
def test_noop_on_single_az():
    test_yaml = get_vars()
    a.testing_startup(test_yaml[0], test_yaml[1],
        micro_single_az_available, high_cpu, friday_midday_update)
    assert(a.result['Action']   ==  'NO_ACTION')
    assert(a.result['Message']  ==  'Unable to work on singleAZ RDS!')

@freeze_time("2016-01-02 19:30:00", tz_offset=0)
def test_increase_on_high_alarm():
    test_yaml = get_vars()
    a.testing_startup(test_yaml[0], test_yaml[1],
        micro_multi_az_available, high_cpu, friday_midday_update)
    assert(a.result['Action']   ==  'RESIZE')
    assert(a.result['Message']  ==  'db.t2.small')

@freeze_time("2016-01-01 19:30:00", tz_offset=0)
def test_in_scheduled_scale_out_micro_to_medium_no_alarm():
    test_yaml = get_vars()
    a.testing_startup(test_yaml[0], test_yaml[1],
        micro_multi_az_available, no_alarm, no_update)
    assert(a.result['Action']   ==  'RESIZE')
    assert(a.result['Message']  ==  'db.m3.medium')

@freeze_time("2016-01-01 19:30:00", tz_offset=0)
def test_in_scheduled_scale_out_medium_to_large_high_alarm():
    test_yaml = get_vars()
    a.testing_startup(test_yaml[0], test_yaml[1],
        medium_multi_az_available, high_cpu, no_update)
    assert(a.result['Action']   ==  'RESIZE')
    assert(a.result['Message']  ==  'db.m4.large')

@freeze_time("2016-01-02 19:30:00", tz_offset=0)
def test_out_scheduled_scale_down_medium_to_small_low_alarm():
    test_yaml = get_vars()
    a.testing_startup(test_yaml[0], test_yaml[1],
        medium_multi_az_available, low_cpu, no_update)
    assert(a.result['Action']   ==  'RESIZE')
    assert(a.result['Message']  ==  'db.t2.small')

@freeze_time("2016-01-02 18:45:00", tz_offset=0)
def test_blocked_recent_down():
    test_yaml = get_vars()
    a.testing_startup(test_yaml[0], test_yaml[1],
        medium_multi_az_available, low_cpu, saturday_midday_update)
    assert(a.result['Action']   ==  'NO_ACTION')
    assert(a.result['Message']  ==  'scale_down Cooldown threshold not reached')

@freeze_time("2016-01-02 18:35:00", tz_offset=0)
def test_blocked_recent_up():
    test_yaml = get_vars()
    a.testing_startup(test_yaml[0], test_yaml[1],
        medium_multi_az_available, high_cpu, saturday_midday_update)
    assert(a.result['Action']   ==  'NO_ACTION')
    assert(a.result['Message']  ==  'scale_up Cooldown threshold not reached')

@freeze_time("2016-01-02 18:55:00", tz_offset=0)
def test_allow_recent_up():
    test_yaml = get_vars()
    a.testing_startup(test_yaml[0], test_yaml[1],
        medium_multi_az_available, high_cpu, saturday_midday_update)
    assert(a.result['Action']   ==  'RESIZE')
    assert(a.result['Message']  ==  'db.m4.large')

@freeze_time("2016-01-02 18:45:00", tz_offset=0)
def test_blocked_busy():
    test_yaml = get_vars()
    a.testing_startup(test_yaml[0], test_yaml[1],
        micro_multi_az_modifying, {}, {})
    assert(a.result['Action']   ==  'NO_ACTION')
    assert(a.result['Message']  ==  'In middle of an operation already!')

@freeze_time("2016-01-02 18:45:00", tz_offset=0)
def test_blocked_unsupported():
    test_yaml = get_vars()
    a.testing_startup(test_yaml[0], test_yaml[1],
        unsupported_multi_az_available, {}, {})
    assert(a.result['Action']   ==  'NO_ACTION')
    assert(a.result['Message']  ==  'Instance size not in list!')

@freeze_time("2016-01-02 18:45:00", tz_offset=0)
def test_scale_up_on_credit_low():
    test_yaml = get_vars()
    a.testing_startup(test_yaml[0], test_yaml[1],
        micro_multi_az_available, credits_low, friday_midday_update)
    assert(a.result['Action']   ==  'RESIZE')
    assert(a.result['Message']  ==  'db.m3.medium')

@freeze_time("2016-01-02 18:45:00", tz_offset=0)
def test_nothing_to_do():
    test_yaml = get_vars()
    a.testing_startup(test_yaml[0], test_yaml[1],
        micro_multi_az_available, no_alarm, no_update)
    assert(a.result['Action']   ==  'NO_ACTION')
    assert(a.result['Message']  ==  'Nothing to do')

@freeze_time("2016-01-02 18:45:00", tz_offset=0)
def test_scaling_disabled_scale_up():
    test_yaml = get_vars('_disabled')
    a.testing_startup(test_yaml[0], test_yaml[1],
        micro_multi_az_available, high_cpu, no_update)
    assert(a.result['Action']   ==  'NO_ACTION')
    assert(a.result['Message']  ==  'Resizing disabled')

@freeze_time("2016-01-02 18:45:00", tz_offset=0)
def test_scaling_disabled_scale_down():
    test_yaml = get_vars('_disabled')
    a.testing_startup(test_yaml[0], test_yaml[1],
        medium_multi_az_available, low_cpu, no_update)
    assert(a.result['Action']   ==  'NO_ACTION')
    assert(a.result['Message']  ==  'Resizing disabled')

@freeze_time("2016-01-01 18:45:00", tz_offset=0)
def test_prevent_scale_down_during_scheduled():
    test_yaml = get_vars()
    a.testing_startup(test_yaml[0], test_yaml[1],
        medium_multi_az_available, low_cpu, no_update)
    assert(a.result['Action']   ==  'NO_ACTION')
    assert(a.result['Message']  ==  'Already at bottom for size during scheduled scale up')

@freeze_time("2016-01-01 19:30:00", tz_offset=0)
def test_invalid_index():
    test_yaml = get_vars('_invalid_index')
    a.testing_startup(test_yaml[0], test_yaml[1],
        medium_multi_az_available, high_cpu, no_update)
    assert(a.result['Action']   ==  'NO_ACTION')
    assert(a.result['Message']  ==  'invalid scheduled_index')

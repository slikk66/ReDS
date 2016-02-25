#!/usr/bin/env python

from troposphere import Template, Parameter, Ref, Join, Output
from troposphere.cloudwatch import Alarm, MetricDimension

t = Template()

rds_instance = t.add_parameter(Parameter(
    'RdsInstance',
    Type='String',
    Description='Instance to monitor'
))

up_threshold = t.add_parameter(
    Parameter(
        'UpThreshold',
        Type='String'
    )
)

up_evaluations = t.add_parameter(
    Parameter(
        'UpEvaluations',
        Type='String'
    )
)

down_threshold = t.add_parameter(
    Parameter(
        'DownThreshold',
        Type='String'
    )
)

down_evaluations = t.add_parameter(
    Parameter(
        'DownEvaluations',
        Type='String'
    )
)

credit_threshold = t.add_parameter(
    Parameter(
        'CreditThreshold',
        Type='String'
    )
)

credit_evaluations = t.add_parameter(
    Parameter(
        'CreditEvaluations',
        Type='String'
    )
)

high_cpu_alarm = t.add_resource(
    Alarm(
        "ReDSAlarmHigh",
        AlarmDescription="CPU High Alarm",
        Namespace="AWS/RDS",
        MetricName="CPUUtilization",
        Statistic="Average",
        Period=60,
        Dimensions=[
            MetricDimension(
                Name="DBInstanceIdentifier",
                Value=Ref(rds_instance)
            )
        ],
        EvaluationPeriods=Ref(up_evaluations),
        Threshold=Ref(up_threshold),
        ComparisonOperator="GreaterThanOrEqualToThreshold",
        AlarmActions=[],
        InsufficientDataActions=[],
        OKActions=[],
    )
)

low_cpu_alarm = t.add_resource(
    Alarm(
        "ReDSAlarmLow",
        AlarmDescription="CPU Low Alarm",
        Namespace="AWS/RDS",
        MetricName="CPUUtilization",
        Statistic="Average",
        Period=60,
        Dimensions=[
            MetricDimension(
                Name="DBInstanceIdentifier",
                Value=Ref(rds_instance)
            )
        ],
        EvaluationPeriods=Ref(down_evaluations),
        Threshold=Ref(down_threshold),
        ComparisonOperator="LessThanOrEqualToThreshold",
        AlarmActions=[],
        InsufficientDataActions=[],
        OKActions=[],
    )
)

low_credit_alarm = t.add_resource(
    Alarm(
        "ReDSNoCredits",
        AlarmDescription="CPU Credits Exhausted Alarm",
        Namespace="AWS/RDS",
        MetricName="CPUCreditBalance",
        Statistic="Maximum",
        Period=60,
        Dimensions=[
            MetricDimension(
                Name="DBInstanceIdentifier",
                Value=Ref(rds_instance)
            )
        ],
        EvaluationPeriods=Ref(credit_evaluations),
        Threshold=Ref(credit_threshold),
        ComparisonOperator="LessThanOrEqualToThreshold",
        AlarmActions=[],
        InsufficientDataActions=[],
        OKActions=[],
    )
)

t.add_output([
    Output(
        'UpAlarm',
        Description='Alarm name for up/high',
        Value=Ref(high_cpu_alarm)
    ),
    Output(
        'DownAlarm',
        Description='Alarm name for down/low',
        Value=Ref(low_cpu_alarm)
    ),
    Output(
        'CreditLowAlarm',
        Description='Alarm name for credits out',
        Value=Ref(low_credit_alarm)
    )
])

if __name__ == '__main__':
    print t.to_json()

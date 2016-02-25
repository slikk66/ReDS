#!/usr/bin/env python

from troposphere import Template, Parameter, iam, Join, Ref, Output, GetAtt
from awacs.aws import Action, Allow, Policy, Principal, Statement

t = Template()

rds_instance = t.add_parameter(Parameter(
    'RdsInstance',
    Type='String',
    Description='Instance to monitor'
))

role = t.add_resource(iam.Role(
    "lambdarole",
    AssumeRolePolicyDocument=Policy(
        Statement=[
            Statement(
                Effect=Allow,
                Principal=Principal('Service', 'lambda.amazonaws.com'),
                Action=[Action('sts', 'AssumeRole')]
            )
        ]
    ),
    Path='/',
    Policies=[iam.Policy(
        'lambdapolicy',
        PolicyName='lambdapolicy',
        PolicyDocument=Policy(
            Statement=[
                Statement(
                    Effect=Allow,
                    Action=[
                        Action('rds', 'DescribeDBInstances'),
                        Action('rds', 'DescribeEvents'),
                    ],
                    Resource=[
                        "*"
                    ]
                ),
                Statement(
                    Effect=Allow,
                    Action=[
                        Action('rds', 'ModifyDBInstance'),
                    ],
                    Resource=[
                        Join('', ['arn:aws:rds:',Ref("AWS::Region"),':',Ref("AWS::AccountId"),':db:',Ref(rds_instance)]),
                    ]
                ),
                Statement(
                    Effect=Allow,
                    Action=[
                        Action('cloudwatch', 'DescribeAlarms'),
                    ],
                    Resource=[
                        "*"
                    ]
                ),
                Statement(
                    Effect=Allow,
                    Action=[
                        Action('logs', 'CreateLogGroup'),
                        Action('logs', 'CreateLogStream'),
                        Action('logs', 'PutLogEvents'),
                    ],
                    Resource=["arn:aws:logs:*:*:*"]
                )
            ]
        )
    )]
))

t.add_output([
    Output(
        'LambdaRole',
        Description='ReDS Lambda Role ARN',
        Value=Ref(role),
    )
])

if __name__ == '__main__':
    print t.to_json()

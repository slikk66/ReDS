#!/usr/bin/env python
from troposphere import Template, Parameter, awslambda, Join, Ref, Output, GetAtt
t = Template()

rds_instance = t.add_parameter(Parameter(
    'RdsInstance',
    Type='String',
    Description='Instance to monitor'
))

lambda_role = t.add_parameter(Parameter(
    'LambdaRole',
    Type='String',
    Description='Lambda Role'
))

bucket_name = t.add_parameter(Parameter(
    'BucketName',
    Type='String',
    Description='Lambda Code Bucket'
))

time_token = t.add_parameter(Parameter(
    'TimeToken',
    Type='String',
    Description='Time Token for last upload'
))

lambda_function = t.add_resource(
    awslambda.Function(
        "reds",
        Code=awslambda.Code(
            S3Bucket=Ref(bucket_name),
            S3Key=Join("",["reds-",Ref(time_token),".zip"])
        ),
        Handler="reds.lambda_handler",
        MemorySize=128,
        Role=Join('',['arn:aws:iam::',Ref("AWS::AccountId"),':role/',Ref(lambda_role)]),
        Runtime="python2.7",
        Timeout=30
    )
)

t.add_output([
    Output(
        'LambdaFunction',
        Description='ReDS Lambda Function',
        Value=Ref(lambda_function),
    )
])

if __name__ == '__main__':
    print t.to_json()

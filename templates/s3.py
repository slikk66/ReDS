#!/usr/bin/env python

from troposphere import GetAtt, Output, Template, Parameter, Ref
from troposphere.s3 import Bucket, Private

t = Template()

s3bucket = t.add_resource(Bucket(
    "code",
    AccessControl=Private
))

t.add_output([
    Output(
        "BucketName",
        Value=Ref(s3bucket),
        Description="ID of Bucket without any DNS"
    )
])

if __name__ == '__main__':
    print t.to_json()

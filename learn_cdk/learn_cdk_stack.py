from aws_cdk import (

    Stack,
    aws_s3 as _s3

)
from constructs import Construct
from pprint import pprint

class LearnCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        _s3.Bucket(self, 'cdk_bucket_01', bucket_name='atula-demo-01', versioned=True, encryption=_s3.BucketEncryption.KMS_MANAGED)
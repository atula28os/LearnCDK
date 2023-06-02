from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as _s3
)

from constructs import Construct

class CdkProj2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        _s3.Bucket(self, 
                   'MyFirstCDKBucket',
                   bucket_name='cdk-proj2-stack',
                   versioned=True,
                   encryption=_s3.BucketEncryption.KMS
                   )

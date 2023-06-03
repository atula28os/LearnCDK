from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as _s3
)

from aws_cdk import CfnOutput

from constructs import Construct

class CdkProj2Stack2(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        _s3.Bucket(self, 
                   'MyFirstCDKBucket',
                   bucket_name='cdk-proj2-stack-0',
                   versioned=True,
                   encryption=_s3.BucketEncryption.KMS
                   )

        s3_bucket = _s3.Bucket(self,
                   id="MySecondCDKBucket",
                   bucket_name='cdk-proj2-stack-1',
                   versioned=True,
                   encryption=_s3.BucketEncryption.KMS)
        
        s3_output = CfnOutput(self, 
                              id='stack-2-bucket-output',
                              value=s3_bucket.bucket_name,
                              description=f'My Second Bucket using CDK',
                              export_name="cdk-bucket2"
                              )
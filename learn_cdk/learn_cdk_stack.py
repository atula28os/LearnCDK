from aws_cdk import (

    Stack,
    aws_s3 as _s3, 
    CfnOutput,

)


from constructs import Construct
from pprint import pprint

class LearnCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        demo01_bucket = _s3.Bucket(self, 'cdk_bucket_01', bucket_name='atula-demo-01', \
                                   versioned=False, \
                                   encryption=_s3.BucketEncryption.KMS_MANAGED)
        
        demo01_output = CfnOutput(self, 's3-demo01-bucket', 
                                value=demo01_bucket.bucket_name,
                                description='atula-demo-01 is my bucket',
                                export_name='s3-demo01' )
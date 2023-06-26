from aws_cdk import (

    Stack,
    aws_s3 as _s3, 
    RemovalPolicy,
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
        
class MyArtifactBucketStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, is_prod=False, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        if is_prod: 
            artifact_bucket = _s3.Bucket(self, 'prod_artifact_bucket', bucket_name='atula-demo-02', versioned=True, 
                                         encryption=_s3.BucketEncryption.S3_MANAGED, 
                                         removal_policy=RemovalPolicy.RETAIN)
        else:
            artifact_bucket = _s3.Bucket(self, 'prod_artifact_bucket', bucket_name='atula-demo-03')
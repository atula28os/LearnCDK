from aws_cdk import (
    Stack,
    CfnOutput,
    aws_s3 as _s3,
    aws_iam as _iam,
    RemovalPolicy,
    Tags,
    Aws
)


from constructs import Construct

class CustomS3ResourceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        demo_bkt = _s3.Bucket(self, 'demo-bucket', 
                              versioned=True,
                              block_public_access=_s3.BlockPublicAccess.BLOCK_ACLS,
                              removal_policy=RemovalPolicy.DESTROY)
        
        demo_bkt.add_to_resource_policy(
            _iam.PolicyStatement(
                effect=_iam.Effect.ALLOW,
                actions=[
                    "s3:GetObject"
                ],
                resources=[demo_bkt.arn_for_objects('*.html')],
                principals=[_iam.AnyPrincipal()]
            )
        )

        demo_bkt.add_to_resource_policy(
            _iam.PolicyStatement(
                effect=_iam.Effect.DENY,
                actions=[
                    "s3:*"
                ],
                resources=[f'{demo_bkt.bucket_arn}/*'],
                principals=[_iam.AnyPrincipal()],
                conditions={
                    "Bool": {"aws:SecureTransport":False}
                }
            )
        )
        
        Tags.of(demo_bkt).add("TypeOfBucket","Demo")
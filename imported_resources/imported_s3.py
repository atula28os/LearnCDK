from aws_cdk import (

    Stack,
    aws_iam as iam,
    aws_s3 as _s3, 
    RemovalPolicy,
    CfnOutput,
    Tags

)

from constructs import Construct

class ImportedS3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        demo01_bucket = _s3.Bucket.from_bucket_name(self, 'demo01-bkt', bucket_name='atula-demo-01')

        policy_statement = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            principals=[iam.AnyPrincipal()],
            actions=["s3:ListBuckets", "s3:GetObject"],
            resources=[demo01_bucket.bucket_arn + '/*']
        )

        demo01_bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.ServicePrincipal("lambda.amazonaws.com")],
                actions=["s3:GetObject"],
                resources=[f"{demo01_bucket.bucket_arn}/*"]
            )
        )

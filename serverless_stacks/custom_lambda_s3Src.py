import json 

from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_s3 as _s3,
    aws_logs as _logs,
    CfnOutput,
    RemovalPolicy,
    Duration
)


from constructs import Construct

class CustomLambdaS3SrcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # try:
                
        #     with open("serverless_stacks/lambda_src/demo_process.py", "r") as file:
        #         demo_code = file.read()
        # except OSError:
        #     print("No such file found")


        # Get S3 Bucket 
        lambda_bucket = _s3.Bucket.from_bucket_name(self, 'lambda-bkt-1', bucket_name='atula-lambda-demo')



        # Create Lambda Bucket
        demo_prc_func = _lambda.Function(self, 'demo-lambda-cfn', 
                                         function_name='demo-lambda-cfn-1',
                                         runtime=_lambda.Runtime.PYTHON_3_9,
                                         handler="demo_process.lambda_handler",
                                         code=_lambda.S3Code(lambda_bucket, key="lambda_src/demo_process.zip"),
                                         timeout=Duration.seconds(10),
                                         reserved_concurrent_executions=5, 
                                         environment={
                                             "LOG_LEVEL": 'INFO'
                                         })

        # Create Custom Log Groups - 
        custom_log_group = _logs.LogGroup(self, "custom_log_group_lambda", 
                                          log_group_name=f"aws/lambda/{demo_prc_func.function_name}",
                                          removal_policy=RemovalPolicy.DESTROY, retention=_logs.RetentionDays.ONE_DAY)
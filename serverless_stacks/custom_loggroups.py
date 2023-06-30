import json 

from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    CfnOutput,
    Duration,
    RemovalPolicy,
    aws_logs as _logs
)


from constructs import Construct

class CustomLambdaLogStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        try:
                
            with open("serverless_stacks/lambda_src/demo_process.py", "r") as file:
                demo_code = file.read()
        except OSError:
            print("No such file found")

        demo_prc_func = _lambda.Function(self, 'demo-lambda-cfn', 
                                         function_name='demo-lambda-cfn',
                                         runtime=_lambda.Runtime.PYTHON_3_9,
                                         handler="index.lambda_handler",
                                         code=_lambda.InlineCode(demo_code), 
                                         timeout=Duration.seconds(10),
                                         reserved_concurrent_executions=5, 
                                         environment={
                                             "LOG_LEVEL": 'INFO'
                                         })
        
        # Create Custom Log Groups - 
        custom_log_group = _logs.LogGroup(self, "custom_log_group_lambda", 
                                          log_group_name=f"aws/lambda/{demo_prc_func.function_name}",
                                          removal_policy=RemovalPolicy.DESTROY)
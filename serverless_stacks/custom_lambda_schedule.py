import json 

from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_events as _events,
    aws_events_targets as event_targets,
    CfnOutput,
    Duration,
    RemovalPolicy,
    aws_logs as _logs
)


from constructs import Construct

class CustomLambdaLogStack2(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        try:
                
            with open("serverless_stacks/lambda_src/demo_process.py", "r") as file:
                demo_code = file.read()
        except OSError:
            print("No such file found")

        demo_prc_func = _lambda.Function(self, 'demo-lambda-cfn', 
                                         function_name='demo-lambda-cfn-2',
                                         runtime=_lambda.Runtime.PYTHON_3_9,
                                         handler="index.lambda_handler",
                                         code=_lambda.InlineCode(demo_code), 
                                         timeout=Duration.seconds(10),
                                         current_version_options=_lambda.VersionOptions(removal_policy=RemovalPolicy.RETAIN, retry_attempts=1),
                                         reserved_concurrent_executions=5, 
                                         environment={
                                             "LOG_LEVEL": 'INFO'
                                         })
        
        # lam_current_version = demo_prc_func.current_version
        # demo_prc_func.add_alias('prod')

        version = demo_prc_func.current_version
        alias = _lambda.Alias(self, "LambdaAliasQA",
            alias_name="QA",
            version=version)

        # Create Custom Log Groups -    
        custom_log_group = _logs.LogGroup(self, "custom_log_group_lambda", 
                                          log_group_name=f"demo/lambda/{demo_prc_func.function_name}",
                                          removal_policy=RemovalPolicy.DESTROY)
        
        # Run Everyday at 18:00 UTC using cron
        six_pm_cron = _events.Rule(self, 'six-pm-cron', schedule=_events.Schedule.cron(
            minute="40", hour="15", month="*", week_day="MON-FRI", year="2023"
        ))

        six_pm_cron.add_target(event_targets.LambdaFunction(demo_prc_func))

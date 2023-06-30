import json 

from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_s3 as _s3,
    aws_iam as _iam,
    aws_dynamodb as ddb, 
    CfnOutput,
    Duration
)


from constructs import Construct

class CustomLambdaS3TestStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        try:
            with open("serverless_stacks/lambda_src/demo_process.py", "r") as file:
                demo_code = file.read()
        except OSError:
            print("No such file found")

        demo_cfn_table = ddb.Table.from_table_name(self, "demo-cfn-table", table_name='demo-cfn')

        demo_lambda = _lambda.Function.from_function_name(self, 'demo-lambda-function', 'demo-lambda-cfn-2')

        version = demo_lambda.latest_version

        demo_cfn_table.grant_read_write_data(demo_lambda)

        

        demo_lambda.add_to_role_policy(statement=_iam.PolicyStatement(
            effect = _iam.Effect.ALLOW,
            resources = [
                demo_cfn_table.table_arn
            ],
          actions = [
                "dynamodb:BatchGetItem",
                "dynamodb:GetRecords",
                "dynamodb:Query",
                "dynamodb:GetItem",
                "dynamodb:ConditionCheckItem",
                "dynamodb:BatchWriteItem",
                "dynamodb:PutItem",
                "dynamodb:UpdateItem",
                "dynamodb:DeleteItem",
                "dynamodb:DescribeTable"
            ],
            principals = [
                _iam.ServicePrincipal('lamda.amazonaws.com')
            ]
        ))


        test_alias = _lambda.Alias(self, 'TestAlias',alias_name='Dev', version=_lambda.Version.from_version_arn(self, "Ver-1", version_arn=f'{demo_lambda.function_arn}:1'))



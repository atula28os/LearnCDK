import json 

from aws_cdk import (
    Stack,
    aws_dynamodb as ddb,
    CfnOutput,
    RemovalPolicy,
    Duration
)


from constructs import Construct

class CustomDDBStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        demo_table = ddb.Table(self, 'demo-table', table_name="demo-cfn", table_class=ddb.TableClass.STANDARD_INFREQUENT_ACCESS, 
                               partition_key=ddb.Attribute(name='id', type=ddb.AttributeType.NUMBER),
                               read_capacity=1,
                               write_capacity=1,
                               removal_policy=RemovalPolicy.DESTROY
                               )

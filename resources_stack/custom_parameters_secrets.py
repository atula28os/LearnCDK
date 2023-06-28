import json

from aws_cdk import (
    Stack,
    CfnOutput,
    Tags,
    aws_secretsmanager as _secretmanager,
    aws_ssm as _ssm

)


from constructs import Construct

class CustomParamStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        param1 = _ssm.StringParameter(self, "param-1", description="param-1", 
                                      parameter_name='param-1', 
                                      string_value="demo-param1",
                                      tier=_ssm.ParameterTier.STANDARD)
        
        ddb_param = _secretmanager.Secret(self, 'db-secret-1',
                                description="mysql db details",
                                secret_name="mysql-db1-ssm",
                                generate_secret_string=_secretmanager.SecretStringGenerator(
                                    secret_string_template=json.dumps(
                                        {
                                            "username": "admin"
                                        }
                                    ),
                                generate_string_key="password"
                                )
                                )
import json

from aws_cdk import (
    Stack,
    CfnOutput,
    Tags,
    aws_secretsmanager as _secretmanager,
    aws_iam as _iam,
    Aws
)


from constructs import Construct

class CustomIamUsersStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        user_1_pwd = _secretmanager.Secret(self, "user-1-pwd", description="user-1 password", secret_name='user_1_pwd')

        user_1 = _iam.User(self, 'iam_user_1', password=user_1_pwd.secret_value, 
                           user_name='demo_user', 
                           password_reset_required=True )
        
        # IAM GROUP
        demo_group = _iam.Group(self, "demo_group", group_name='DemoGroup')

        # Add USer
        demo_group.add_user(user_1)

        # Add Managed Policy to Group
        demo_group.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3ReadOnlyAccess')
        )
        

        #Add Statement to Group - Method 2
        ssm_describe_stmt = _iam.PolicyStatement(
            actions=["ssm:ListDocuments",
                "ssm:ListDocumentVersions",
                "ssm:DescribeDocument",
                "ssm:GetDocument",
                "ssm:DescribeParameter",
                "ssm:DescribeInstanceInformation",
                "ssm:DescribeDocumentParameters",
                "ssm:DescribeInstanceProperties"],
            resources=['*'],
            effect=_iam.Effect.ALLOW,
            sid="Describe SSM Paramter"
        )

        demo_group.add_to_policy(ssm_describe_stmt)


        #Create  a role
        demo_dev_role = _iam.Role(self, 'demo-role-01', 
                                  assumed_by=_iam.AccountPrincipal(f'{Aws.ACCOUNT_ID}'),
                                  role_name='demo-dev-role')
        
        #Create Managed Policy & Add to Role
        list_ec2_policy = _iam.ManagedPolicy(self, 
                                             "listEc2Instances",
                                             description='list ec2 instances',
                                             managed_policy_name='list_ec2_demo_policy',
                                             statements=[_iam.PolicyStatement(
                                                effect=_iam.Effect.ALLOW,
                                                actions=[
                                                    "ec2:Describe*",
                                                    "cloudwatch:Describe*",
                                                    "cloudwatch:Get*"
                                                ],
                                                resources=["*"]
                                             )],
                                             roles=[
                                                 demo_dev_role
                                             ])

        #Add Tag to User
        Tags.of(user_1).add('UserType', 'TestUser')



        #Output 
        user_1_output = CfnOutput(self, 'user-1-output', 
                                  description="User-1 Login Details",
                                  value=f"https://{Aws.ACCOUNT_ID}.signin.aws.amazon.com/console")
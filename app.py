#!/usr/bin/env python3
import os

import aws_cdk as cdk

from learn_cdk.learn_cdk_stack import LearnCdkStack, MyArtifactBucketStack, LearnCdkStack2
from resources_stack.custom_vpc import LearnVpcStack
from resources_stack.custom_ec2 import CustomEc2Stack
from resources_stack.custom_ec2_instance_profile import CustomEc2InstanceProfileStack

from imported_resources.imported_s3 import ImportedS3Stack

app = cdk.App()

prod_account = app.node.try_get_context('envs')['prod']['account']
prod_region = app.node.try_get_context('envs')['prod']['region']

dev_account = app.node.try_get_context('envs')['dev']['account']
dev_region = app.node.try_get_context('envs')['dev']['region']

# LearnCdkStack(app, "LearnCdkStack",
#     #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
#     env=cdk.Environment(account=account, region=region),
#     )

# MyArtifactBucketStack(app, "MyDevArtifactBucketStack")

# MyArtifactBucketStack(app, "MyProdArtifactBucketStack", is_prod=True, env=cdk.Environment(account=prod_account, region=prod_region))

# LearnVpcStack(app, "LearnVpcStack")

# LearnCdkStack2(app, "LearnCdkStack2")

# ImportedS3Stack(app, "ImportedS3Stack")

# CustomEc2Stack(app, "CustomEc2Stack-01", env=cdk.Environment(account=dev_account, region=dev_region))

CustomEc2InstanceProfileStack(app, "CustomEc2Stack-02", env=cdk.Environment(account=dev_account, region=dev_region))

app.synth()

#!/usr/bin/env python3
import os

import aws_cdk as cdk

from learn_cdk.learn_cdk_stack import LearnCdkStack, MyArtifactBucketStack

app = cdk.App()

prod_account = app.node.try_get_context('prod')['account']
prod_region = app.node.try_get_context('prod')['region']

# LearnCdkStack(app, "LearnCdkStack",
#     #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
#     env=cdk.Environment(account=account, region=region),
#     )

# MyArtifactBucketStack(app, "MyDevArtifactBucketStack")

MyArtifactBucketStack(app, "MyProdArtifactBucketStack", is_prod=True, env=cdk.Environment(account=prod_account, region=prod_region))

app.synth()

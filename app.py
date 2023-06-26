#!/usr/bin/env python3
import os

import aws_cdk as cdk

from learn_cdk.learn_cdk_stack import LearnCdkStack, MyArtifactBucketStack

app = cdk.App()

# LearnCdkStack(app, "LearnCdkStack",

#     #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

#     env=cdk.Environment(account='997403957483', region='us-east-1'),
#     )

MyArtifactBucketStack(app, "MyDevArtifactBucketStack")
MyArtifactBucketStack(app, "MyProdArtifactBucketStack", is_prod=True)

app.synth()

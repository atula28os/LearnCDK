#!/usr/bin/env python3
import os

import aws_cdk as cdk

from learn_cdk.learn_cdk_stack import LearnCdkStack


app = cdk.App()
LearnCdkStack(app, "LearnCdkStack",

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    env=cdk.Environment(account='997403957483', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()

import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_proj2.cdk_proj2_stack import CdkProj2Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_proj2/cdk_proj2_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkProj2Stack(app, "cdk-proj2")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

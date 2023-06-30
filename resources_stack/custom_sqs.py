from aws_cdk import (
    Stack,
    aws_sqs as _sqs,
    CfnOutput,
    Duration
)


from constructs import Construct

class CustomSQSStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        demo_queue = _sqs.Queue(self, 'demo-sqs', 
                                queue_name='demo-queue.fifo', 
                                fifo=True, 
                                encryption=_sqs.QueueEncryption.KMS_MANAGED,
                                visibility_timeout=Duration.seconds(45),
                                retention_period=Duration.hours(1))
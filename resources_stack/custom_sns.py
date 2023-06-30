from aws_cdk import (
    Stack,
    aws_sns as _sns,
    aws_sns_subscriptions as sns_subs,
    CfnOutput,
    Duration
)


from constructs import Construct

class CustomSnsStack2(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        demo_sns_topic = _sns.Topic(self, 'hot-topics', display_name='Latest Dev Topics', topic_name='dev-hot-topic')

        demo_sns_topic.add_subscription(sns_subs.EmailSubscription('atula28os@gmail.com'))


        

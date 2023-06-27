from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as _ec2,
    Tags
)


from constructs import Construct

class CustomEc2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        demo_vpc = _ec2.Vpc.from_lookup(self, 'demo-vpc', vpc_id='vpc-0dc90dc63720a8bbe')


        #Read Bootstrap 
        with open("bootstrap_scripts/install_httpd.sh", "r") as file:
            user_data = file.read()


        web_server = _ec2.Instance(self, "webserver", 
                                   instance_name='webserverId-01',
                                   instance_type=_ec2.InstanceType.of(_ec2.InstanceClass.T2, _ec2.InstanceSize.MICRO),
                                   machine_image=_ec2.AmazonLinuxImage(generation=_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
                                   vpc=demo_vpc,
                                   vpc_subnets=_ec2.SubnetSelection(subnet_type=_ec2.SubnetType.PUBLIC),
                                   user_data=_ec2.UserData.custom(user_data)
                                   )

        web_server_output = CfnOutput(self, 'webserver01-output', 
                                      description="webserver Public Ip Address", 
                                      value=f'http://{web_server.instance_public_ip}',
                                      export_name="webserver-pub-ip")
        
        #Allow Traffic from anywhere to Webserver
        web_server.connections.allow_from_any_ipv4(_ec2.Port.tcp(80), description="Allow Web Traffic")
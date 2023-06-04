
from aws_cdk import (Stack, 
                     aws_ec2 as _ec2,
                     CfnOutput,
                     CfnTag,
                     Tags,
                     
                     )

from constructs import Construct

class CdkProjEc2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        custom_vpc = _ec2.Vpc.from_lookup(self, "vpc-test-id", vpc_id='vpc-01e5a7f6090b613be')
        

        with open("bootstrap_scripts/install_httpd.sh", mode="r") as file:
            user_data = file.read()

        custom_ec2 = _ec2.Instance(self, "CDKInstance", 
                                   instance_type=_ec2.InstanceType.of(_ec2.InstanceClass.BURSTABLE2, _ec2.InstanceSize.MICRO),
                                    machine_image=_ec2.MachineImage.latest_amazon_linux(
                                        generation=_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
                                    ),
                                   vpc=custom_vpc,
                                   vpc_subnets=_ec2.SubnetSelection(subnet_type=_ec2.SubnetType.PUBLIC ),
                                   user_data=_ec2.UserData.custom(user_data))
        
        ec2_output = CfnOutput(self, 'webserver-output',
                             description="Webserver Public IP", 
                             value=f"http://{custom_ec2.instance_public_ip}"
                               )
        
        #Allow Public Traffic using Security Group
        custom_ec2.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(80), description="allow web traffic"
        )
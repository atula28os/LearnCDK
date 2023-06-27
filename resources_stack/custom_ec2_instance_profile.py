from aws_cdk import (
    Stack,
    CfnOutput,
    aws_iam as iam,
    aws_ec2 as _ec2,
    Tags,
    Size
)


from constructs import Construct

class CustomEc2InstanceProfileStack(Stack):

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

        web_server.role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
        web_server.role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess"))

        volume = _ec2.Volume(self, "EBS-Volume",
            availability_zone="us-east-1a",
            size=Size.gibibytes(500),
            encrypted=True
        )

        volume.grant_attach_volume_by_resource_tag(web_server.grant_principal, [web_server])
        target_device = "/dev/xvdz"
        web_server.user_data.add_commands("TOKEN=$(curl -SsfX PUT \"http://169.254.169.254/latest/api/token\" -H \"X-aws-ec2-metadata-token-ttl-seconds: 21600\")", "INSTANCE_ID=$(curl -SsfH \"X-aws-ec2-metadata-token: $TOKEN\" http://169.254.169.254/latest/meta-data/instance-id)", f"aws --region {Stack.of(self).region} ec2 attach-volume --volume-id {volume.volumeId} --instance-id $INSTANCE_ID --device {target_device}", f"while ! test -e {target_device}; do sleep 1; done")
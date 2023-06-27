from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as _ec2,
    aws_iam as _iam,
    aws_elasticloadbalancingv2 as elbv2,
    aws_autoscaling as _autoscaling,
    Tags,
    Size
)


from constructs import Construct

class CustomEc2AlbStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        dev_vpc_config = self.node.try_get_context('envs')['dev']['vpc_configs']

        # Read Bootstrap Script 
        try:
            with open('bootstrap_scripts/install_httpd.sh', 'r') as bootfile:
                user_data = bootfile.read()
        except OSError:
            print("Not able to find/read the bootstrap script")



        dev_vpc = _ec2.Vpc(self, 'dev-vpc-atula', 
                            enable_dns_hostnames=True, 
                            enable_dns_support=True, 
                            ip_addresses=_ec2.IpAddresses.cidr(dev_vpc_config['vpc_cidr']),
                            vpc_name='dev-vpc',
                            nat_gateways=1, 
                            max_azs=2,
                            subnet_configuration=[
                                 _ec2.SubnetConfiguration(name="dev-vpc-pub-sub", subnet_type=_ec2.SubnetType.PUBLIC),
                                _ec2.SubnetConfiguration(name="dev-vpc-prv-sub", subnet_type=_ec2.SubnetType.PRIVATE_WITH_EGRESS),
                            ]
                            )
        
        # Add Security Group
        dev_sgp = _ec2.SecurityGroup(self, "dev-security-group", vpc=dev_vpc, description="Allow all traffic on port 80")
        
        dev_sgp.add_egress_rule(
            peer=_ec2.Peer.ipv4('0.0.0.0/16'),
            connection=_ec2.Port.tcp(80)
        )

        dev_sgp.add_egress_rule(
            peer=_ec2.Peer.any_ipv4(),
            connection=_ec2.Port.tcp(22)
        )

        dev_sgp.add_ingress_rule(
            peer=_ec2.Peer.ipv4('0.0.0.0/16'),
            connection=_ec2.Port.tcp(80)
        )

        dev_sgp.add_ingress_rule(
            peer=_ec2.Peer.any_ipv4(),
            connection=_ec2.Port.tcp(22)
        )

        dev_web_server = _ec2.Instance(self, 'dev-web-server-01',
                                       instance_name='dev-web-server-01',
                                       instance_type=_ec2.InstanceType.of(_ec2.InstanceClass.T2, _ec2.InstanceSize.MICRO),
                                       machine_image=_ec2.AmazonLinuxImage(generation=_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
                                       vpc=dev_vpc,
                                       block_devices=[_ec2.BlockDevice(
                                                    device_name="/dev/sda1",
                                                    volume=_ec2.BlockDeviceVolume.ebs(50)
                                                )],
                                        security_group=dev_sgp
                                        )

        #Allow connection to EC2 instance 
        dev_web_server.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(80), "Allow Connection on Port 80"
        )

        dev_web_server.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(22), "Allow SSH Connection from anywhere"
        )

        # Create ALB
        dev_alb = elbv2.ApplicationLoadBalancer(self,"dev-alb", vpc=dev_vpc, internet_facing=True, load_balancer_name='dev-webserver-alb')

        # Allow ALB to receive internet traffic
        dev_alb.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(80), description='Allow Internet Access on ALB Port 80'
        )

        # Add Listner to ALB
        listner = dev_alb.add_listener("listnetId", port=80, open=True)

        #Webserver IAM Role
        dev_webserver_role = _iam.Role(self, "dev-webserver-role", 
                                       assumed_by=_iam.ServicePrincipal('ec2.amazonaws.com'), 
                                       managed_policies=[
                                           _iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSSMManagedInstanceCore'),
                                           _iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3ReadOnlyAccess')
                                       ])
        
        # Create Auto Scaling Group with 2 EC2s
        dev_webserver_asg = _autoscaling.AutoScalingGroup(self, 'dev-webserver-asg', 
                                                          vpc=dev_vpc, 
                                                          instance_type=_ec2.InstanceType.of(_ec2.InstanceClass.T2, _ec2.InstanceSize.MICRO),
                                                          machine_image=_ec2.AmazonLinuxImage(generation=_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
                                                          role=dev_webserver_role,
                                                          min_capacity=2,
                                                          max_capacity=4,
                                                          desired_capacity=2,
                                                          user_data=_ec2.UserData.custom(user_data))   
        
        # Add connection to ASG
        dev_webserver_asg.connections.allow_from(
            dev_alb, _ec2.Port.tcp(80), description="Allow ASG receive traffic from ALB"
        )

        listner.add_targets("listnerId", port=80, targets=[dev_webserver_asg])


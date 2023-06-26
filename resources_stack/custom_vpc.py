from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as _ec2
)


from constructs import Construct

class LearnVpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        prod_config = self.node.try_get_context('envs')['prod']
        vpc_config = prod_config['vpc_configs']
        
        custom_vpc = _ec2.Vpc(self, "CustomVpc-02", \
                              ip_addresses=_ec2.IpAddresses.cidr(vpc_config['vpc_cidr']), \
                              max_azs=2,
                              nat_gateways=1,
                              enable_dns_hostnames=True,
                              enable_dns_support=True,
                              subnet_configuration=[ _ec2.SubnetConfiguration(name='public-subnets', cidr_mask=vpc_config['cidr_mask'], \
                                                                              subnet_type=_ec2.SubnetType.PUBLIC),
                                                     _ec2.SubnetConfiguration(name='private-subnets', cidr_mask=vpc_config['cidr_mask'], \
                                                                              subnet_type=_ec2.SubnetType.PRIVATE_WITH_EGRESS),
                                                     _ec2.SubnetConfiguration(name='db-subnets', cidr_mask=vpc_config['cidr_mask'], \
                                                                              subnet_type=_ec2.SubnetType.PRIVATE_ISOLATED)
                                                    
                                                    ]
                              
                              )
        
        vpc_output = CfnOutput(self, 'custom-vpc-output', value=custom_vpc.vpc_id, 
                               description='Custom VPC using CDK', \
                               export_name='custom-vpc-output')
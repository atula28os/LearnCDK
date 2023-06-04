
from aws_cdk import (Stack, 
                     aws_ec2 as _ec2,
                     CfnOutput,
                     CfnTag,
                     Tags,
                     
                     )

from constructs import Construct

class CdkProjVpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc_config = self.node.try_get_context('VPC')

        custom_vpc = _ec2.Vpc(self, 
                              "VpcUsingCdk",
                              ip_addresses=_ec2.IpAddresses.cidr(vpc_config['vpc_cidr']),
                              max_azs=2,
                              nat_gateways=1,
                              subnet_configuration=[
                                  _ec2.SubnetConfiguration(name="pub-subnet",
                                                           cidr_mask=vpc_config['cidr_mask'],
                                                           subnet_type=_ec2.SubnetType.PUBLIC),
                                  _ec2.SubnetConfiguration(name="prv-subnet",
                                                           cidr_mask=vpc_config['cidr_mask'],
                                                           subnet_type=_ec2.SubnetType.PRIVATE_WITH_EGRESS),
                                    _ec2.SubnetConfiguration(name="db-subnet",
                                                           cidr_mask=vpc_config['cidr_mask'],
                                                           subnet_type=_ec2.SubnetType.PRIVATE_ISOLATED)          
                              ]

                        
                              )
        
        Tags.of(custom_vpc).add("Env-Type", "Dev")

        vpc_output = CfnOutput(self,
                               "custom-vpc-output",
                               value=custom_vpc.vpc_id,
                               export_name="custom-vpc-id")

        vpc2 = _ec2.Vpc.from_vpc_attributes(self, "imported-vpc", vpc_id='vpc-ead37097',availability_zones=['us-east-1a','us-east-1d', 'us-east-1f'] )

        vpc2_output =CfnOutput(self, "imported-vpc-output", value=vpc2.vpc_id, export_name='imported-vpc2')

        vpc_peer = _ec2.CfnVPCPeeringConnection(self, "vpc-peer-default-custom1", 
                                                peer_vpc_id=vpc2.vpc_id,
                                                vpc_id=custom_vpc.vpc_id,
                                                tags=[CfnTag(key="Env-Type", value="Dev")]
                                                )
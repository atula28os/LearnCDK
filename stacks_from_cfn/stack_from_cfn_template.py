import json 

from aws_cdk import (
    Stack,
    cloudformation_include as cfn_inc,
    CfnOutput
)


from constructs import Construct

class StackFromCloudFormationTemplate(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        resource_from_cfn_temp = cfn_inc.CfnInclude(self, "DemoInfraTemplate", 
                                                    template_file="stacks_from_cfn/sample_templates/create_s3_bucket_template.json")
        
        encrypted_bucket = resource_from_cfn_temp.get_resource("EncryptedS3Bucket")
        encrypted_bucket_arn = encrypted_bucket.attr_arn

        encrypt_bkt_output  = CfnOutput(self, "encrypt-bkt-output", value=f"{encrypted_bucket_arn}", 
                                        description="Encrypted Bucket Arn",
                                        export_name="bkt-arn")
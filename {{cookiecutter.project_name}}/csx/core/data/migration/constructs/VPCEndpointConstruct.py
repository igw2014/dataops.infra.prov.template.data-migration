from cdktf import TerraformOutput, S3Backend
from constructs import Construct

from imports.aws.data_aws_security_group import DataAwsSecurityGroup
from imports.aws.data_aws_vpc import DataAwsVpc
from imports.aws.provider import AwsProvider
from imports.aws.security_group_rule import SecurityGroupRule
from imports.aws.vpc_endpoint import VpcEndpoint


class VPCEndpointConstruct(Construct):
    data_aws_vpc: DataAwsVpc

    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        #AWS provider to be picked up from tfvars file - default-should not be changed by user
        #region and profile to be picked up from tfvars file - user input
        # vpc id to come as input from user in tfvars file
        # id_ ro be prefixed base don prefix provided by user in tfvars file
        #service_name,endpoint type to be hardcoded as they are not supposed to be configurable
        #route table id to come from as input from user through tfcars file

        AwsProvider(self, "AWS", region="eu-west-1", profile="syncron")
        data_aws_vpc = DataAwsVpc(
            id="vpc-0c01c4e43d938b89d",
            scope=scope,
            id_='data_aws_vpc'
        )

        vpc_endpoint = VpcEndpoint(
            vpc_id=data_aws_vpc.id,
            service_name="com.amazonaws.us-east-1.s3",
            vpc_endpoint_type="Gateway",
            route_table_ids=["rtb-05fdcda96f768a274"],
            scope=scope,
            id_="vpc_endpoint"
        )

        #id_ should be change ,should you need to add another vpcendpoint
        TerraformOutput(self, "vpc_endpoint_construct_output",
                        value=[vpc_endpoint.vpc_endpoint_type],
                        )
        #bucket name should get generated during module creation and jinja template should be replaced by input from user
        #input should be cat-dev<customer or tenant name>-<environment>
        #region should also come as input from user during module creation
        #if difficult to templatize then pick from prop file or tfvars
        S3Backend(self,
                  bucket="cat-dev-network",
                  key="vpc-endpoint/terraform.tfstate",
                  encrypt=True,
                  region="us-east-1"
                  )
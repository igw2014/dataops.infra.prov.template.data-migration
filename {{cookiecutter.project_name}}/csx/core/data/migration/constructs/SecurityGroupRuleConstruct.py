from cdktf import TerraformOutput, S3Backend
from constructs import Construct

from csx.core.data.migration.variables.CommonVariables import CommonVariables
from csx.core.data.migration.variables.NetworkInfraVariables import NetworkInfraVariables
from imports.aws.data_aws_security_group import DataAwsSecurityGroup
from imports.aws.provider import AwsProvider
from imports.aws.security_group_rule import SecurityGroupRule


class SecurityGroupRuleConstruct(Construct):
    # data_aws_vpc: DataAwsVpc

    def __init__(self, scope: Construct, id: str,common_vars:CommonVariables,network_vars:NetworkInfraVariables):
        super().__init__(scope, id)

        #AWS provider to be picked up from tfvars file - default-should not be changed by user
        #region and profile to be picked up from tfvars file - user input
        # vpc id to come as input from user in tfvars file
        # id_ ro be prefixed base don prefix provided by user in tfvars file
        #service_name,endpoint type to be hardcoded as they are not supposed to be configurable
        #route table id to come from as input from user through tfcars file
        region = common_vars.__get_region__()[1:-1][:-1]
        profile = common_vars.__get_profile__()[1:-1][:-1]
        security_group_id = network_vars.__get_security_group_id__()[1:-1][:-1]
        cidr_blocks = network_vars.__get_cidr_blocks__()[1:-1]
        folder = common_vars.__get_s3_key__()[1:-1][:-1]
        bucket = common_vars.__get_s3_bucket__()[1:-1][:-1]
        # above provision was done because terraform variables not working so reading tfvars as file
        AwsProvider(self, "AWS", region=region, profile=profile)
        # data_aws_vpc = DataAwsVpc(
        #     id="vpc-0f1173895f32ddf98",
        #     scope=scope,
        #     id_='data_aws_vpc_1'
        # )

        data_aws_security_group_custom = DataAwsSecurityGroup(
            id=security_group_id,
            scope=scope,
            id_='data_aws_security_group_custom'
        )
        # cidr blocks for dms private ip and ec2 ssh tunnel private ip should come form user as input
        # user can get dms private ip from tf o/p and ec2 private ip from aws console
        rds_dms_ingress_custom = SecurityGroupRule(
                type="ingress",
                from_port=0,
                to_port=0,
                protocol="All",
                cidr_blocks=[cidr_blocks],
                security_group_id=data_aws_security_group_custom.id,
                scope=scope,
                id_="rds_dms_ingress_custom"
        )
        #id_ should be change ,should you need to add another vpcendpoint
        TerraformOutput(self, "sec_grp_rule_construct_output",
                        value=[],
                        )
        #bucket name should get generated during module creation and jinja template should be replaced by input from user
        #input should be cat-dev<customer or tenant name>-<environment>
        #region should also come as input from user during module creation
        #if difficult to templatize then pick from prop file or tfvars
        # 2 constructs under same stack cant have different bucket/states hence the state for these resources have to be shared
        # between tenants.For now keep the bucket as some common name not spec to tenant

        key = folder+"/terraform.tfstate"

        S3Backend(self,
                  bucket=bucket,
                  key=key,
                  encrypt=True,
                  region=region
                  )
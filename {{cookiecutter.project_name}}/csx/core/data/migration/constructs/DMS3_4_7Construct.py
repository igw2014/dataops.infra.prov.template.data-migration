import json

from cdktf import TerraformOutput, S3Backend
from constructs import Construct

from csx.core.data.migration.variables.DMS3_4_7_InfraVariables import DMS3_4_7_InfraVariables
from csx.core.data.migration.variables.CommonVariables import CommonVariables
from csx.core.data.migration.variables.DatabaseInfraVariables import DatabaseInfraVariables
from csx.core.data.migration.variables.NetworkInfraVariables import NetworkInfraVariables
from imports.aws.data_aws_iam_policy import DataAwsIamPolicy
from imports.aws.data_aws_security_group import DataAwsSecurityGroup
from imports.aws.data_aws_vpc import DataAwsVpc
from imports.aws.dms_endpoint import DmsEndpoint
from imports.aws.dms_replication_instance import DmsReplicationInstance
from imports.aws.dms_replication_task import DmsReplicationTask
from imports.aws.iam_role import IamRole
from imports.aws.iam_role_policy_attachment import IamRolePolicyAttachment
from imports.aws.provider import AwsProvider
from imports.aws.s3_bucket import S3Bucket
from imports.aws.s3_bucket_public_access_block import S3BucketPublicAccessBlock


class DMS3_4_7Construct(Construct):
    data_aws_vpc: DataAwsVpc

    def __init__(self, scope: Construct, id: str
                 , common_vars: CommonVariables
                 , network_infra_vars: NetworkInfraVariables
                 , dms3_4_7_vars: DMS3_4_7_InfraVariables
                 , database_infra_variables: DatabaseInfraVariables):
        super().__init__(scope, id)
        region = common_vars.__get_region__()[1:-1][:-1]
        profile = common_vars.__get_profile__()[1:-1][:-1]
        data_migration_s3_folder = common_vars.__get_data_migration_s3_key__()[1:-1][:-1]
        bucket = common_vars.__get_tf_state_s3_bucket__()[1:-1][:-1]
        tenant = common_vars.__get_tenant__()[1:-1][:-1]
        env_prefix = common_vars.__get_env_prefix__()[1:-1][:-1]
        vpc_id = network_infra_vars.__get_vpc_id__()[1:-1][:-1]
        security_group_id = network_infra_vars.__get_dms_security_group_id__()[1:-1][:-1]
        dms_security_group_id = network_infra_vars.__get_dms_security_group_id__()[1:-1][:-1]
        data_replication_engine_name = dms3_4_7_vars.__get_data_replication_engine_name__()[1:-1][:-1]
        source_name = dms3_4_7_vars.__get_source_name__()[1:-1][:-1]
        db_name = database_infra_variables.__get_db_name__()[1:-1][:-1]
        db_master_user = database_infra_variables.__get_db_master_user__()[1:-1][:-1]
        db_master_pwd = database_infra_variables.__get_db_master_pwd__()[1:-1][:-1]
        server_name = database_infra_variables.__get_server_name__()[1:-1][:-1]
        target_name = dms3_4_7_vars.__get_target_name__()[1:-1][:-1]
        migration_type = dms3_4_7_vars.__get_migration_type__()[1:-1][:-1]
        data_replication_task_name = dms3_4_7_vars.__get_data_replication_task_name__()[1:-1][:-1]
        schema_name = dms3_4_7_vars.__get_schema_name__()[1:-1][:-1]
        table_name = dms3_4_7_vars.__get_table_name__()[1:-1][:-1]

        # AWS provider to be picked up from tfvars file - default-should not be changed by user
        # region and profile to be picked up from tfvars file - user input
        # vpc id to come as input from user in tfvars file
        # id_ ro be prefixed base don prefix provided by user in tfvars file
        # service_name,endpoint type to be hardcoded as they are not supposed to be configurable
        # route table id to come from as input from user through tfcars file

        AwsProvider(self, "AWS", region=region, profile=profile)
        data_aws_vpc = DataAwsVpc(
            id=vpc_id,
            scope=scope,
            id_='data_aws_vpc'
        )
        # sg to be created for this stack purpose ie for db
        data_aws_security_group = DataAwsSecurityGroup(
            id=dms_security_group_id,
            scope=scope,
            id_='data_aws_security_group'
        )

        # allocated storage to be set to minimum for dev licenece and hardcoded
        # allocated storage to come from user for test licence via doc prepared by dev team
        # QA to co-ordicate for load testing/stress to find the limit per size involved
        # replicatoin instance class to also follow above strategy
        # multi_az to be false for dev and true for staging and prod env, to be provided as input by user in tfvars file
        # engine version not configurable hence hardcoded
        # cat-dev to come as a prefic from user as input
        data_replication_engine_name = data_replication_engine_name + '-' + tenant + '-' + env_prefix + '-dops-repl-inst'
        dms_replication_instance = DmsReplicationInstance(
            allocated_storage=1,
            apply_immediately=True,
            auto_minor_version_upgrade=True,
            replication_instance_class="dms.t3.medium",
            multi_az=False,
            engine_version="3.4.7",
            publicly_accessible=False,
            replication_instance_id=data_replication_engine_name,
            vpc_security_group_ids=[data_aws_security_group.id],
            scope=scope,
            id_="dms_replication_instance"
        )

        # endpoint id to be combine with prefix provided by user as input
        # ,user,pwd should come from user as input
        # database name,server name tso be captured from tf o/p
        source_name = source_name + '-' + tenant + '-' + env_prefix + '-dops-postgresql-src'
        dms_source_endpoint = DmsEndpoint(
            endpoint_type="source",
            endpoint_id=source_name,
            database_name=db_name,
            engine_name="aurora-postgresql",
            username=db_master_user,
            password=db_master_pwd,
            server_name=server_name,
            port=5432,
            scope=scope,
            id_="dms_source_endpoint"
        )

        # s3 access needs to be more fine grained,use managed policy instead of aws policy later
        data_aws_iam_policy = DataAwsIamPolicy(
            name="AmazonS3FullAccess",
            scope=scope,
            id_="data_aws_iam_policy"
        )
        # cat-dev to come from prefix as user input
        dms_s3_target_iam_role = IamRole(
            name=tenant + '-' + env_prefix + "-dops-dms-s3-access-role",
            scope=scope,
            id_=tenant + '-' + env_prefix + "-dops-dms-s3-access-role",
            assume_role_policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "",
                        "Action": "sts:AssumeRole",
                        "Principal": {
                            "Service": "dms.amazonaws.com"
                        },
                        "Effect": "Allow",
                    },
                ],
            }),
        )

        iam_role_policy_attachment = IamRolePolicyAttachment(
            role=dms_s3_target_iam_role.name,
            policy_arn=data_aws_iam_policy.arn,
            scope=scope,
            id_="iam_role_policy_attachment"
        )

        # cat-dev to come from user input as prefix
        target_s3_bucket = S3Bucket(
            bucket=target_name + '-' + tenant + '-' + env_prefix,
            scope=scope,
            id_="target_s3_bucket"
        )

        # always create private bucket for security compliance
        target_s3_bucket_public_access_block = S3BucketPublicAccessBlock(
            bucket=target_s3_bucket.id,
            block_public_acls=True,
            block_public_policy=True,
            ignore_public_acls=True,
            restrict_public_buckets=True,
            scope=scope,
            id_="target_s3_bucket_public_access_block"
        )

        # except cat-dev prefix nothing else is configurable
        target_name = target_name + '-' + tenant + '-' + env_prefix + '-dops-s3-target'
        dms_target_endpoint = DmsEndpoint(
            endpoint_type="target",
            endpoint_id=target_name,
            s3_settings={
                "bucket_name": target_s3_bucket.bucket,
                "service_access_role_arn": dms_s3_target_iam_role.arn,
                "add_column_name": True,
                "timestamp_column_name": target_name + '_' + tenant + '_' + env_prefix + "_timestamp_cdc"
            },
            engine_name="s3",
            scope=scope,
            id_="dms_target_endpoint"
        )

        # only cat-dev prefix and schema name and comma separated tables names to be included or excluded will come
        # as input " other configs to be hardcoded not configurable" no extra format or layer of json for accepting
        # usr input or table info no additional input accepting dsl to be developed here,just accept the input and
        # pass it to construct as needed the below config is minimal,to be enhanced on need basis

        if migration_type == '1':
            migration_type = 'cdc'
        else:
            migration_type = 'full-load-and-cdc'
        dms_replication_task = DmsReplicationTask(
            migration_type=migration_type,
            replication_instance_arn=dms_replication_instance.replication_instance_arn,
            replication_task_id=data_replication_task_name + '-' + tenant + '-' + env_prefix,
            source_endpoint_arn=dms_source_endpoint.endpoint_arn,
            target_endpoint_arn=dms_target_endpoint.endpoint_arn,
            scope=scope,
            id_="dms_replication_task",
            table_mappings="{\"rules\":[{\"rule-type\":\"selection\",\"rule-id\":\"1\",\"rule-name\":\"1\","
                           "\"object-locator\":{\"schema-name\":"+schema_name+",\"table-name\":"+table_name+"\"},"
                                                                              "\"rule-action\":\"include\"}]}",
            replication_task_settings="{\"Logging\":{\"EnableLogging\":false}}"
        )

        TerraformOutput(self, "dms_3_4_7_construct_output",
                        value=[dms_replication_instance.replication_instance_private_ips
                            , dms_replication_task.replication_task_arn
                            , dms_replication_instance.replication_instance_arn
                            , dms_source_endpoint.endpoint_arn
                            , dms_target_endpoint.endpoint_arn],
                        )
        key = data_migration_s3_folder + "/terraform.tfstate"
        S3Backend(self,
                  bucket=tenant+'-'+env_prefix+bucket,
                  key=key,
                  encrypt=True,
                  region=region
                  )

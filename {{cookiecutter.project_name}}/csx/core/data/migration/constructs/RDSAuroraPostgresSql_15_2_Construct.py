from cdktf import TerraformOutput, S3Backend
from constructs import Construct

from csx.core.data.migration.variables.CommonVariables import CommonVariables
from csx.core.data.migration.variables.DatabaseInfraVariables import DatabaseInfraVariables
from csx.core.data.migration.variables.NetworkInfraVariables import NetworkInfraVariables
from imports.aws.data_aws_security_group import DataAwsSecurityGroup
from imports.aws.data_aws_subnets import DataAwsSubnetsFilter, DataAwsSubnets
from imports.aws.data_aws_vpc import DataAwsVpc
from imports.aws.db_subnet_group import DbSubnetGroup
from imports.aws.provider import AwsProvider
from imports.aws.rds_cluster import RdsCluster
from imports.aws.rds_cluster_instance import RdsClusterInstance
from imports.aws.rds_cluster_parameter_group import RdsClusterParameterGroupParameter, RdsClusterParameterGroup


# to add a new resource make sure that you provide a different id_ while scope remains same

class RDSAuroraPostgresSql_15_2_Construct(Construct):

    def __init__(self, scope: Construct, id: str
                 , common_vars: CommonVariables
                 , network_inra_vars: NetworkInfraVariables
                 , database_infra_variables: DatabaseInfraVariables):
        super().__init__(scope, id)

        region = common_vars.__get_region__()[1:-1][:-1]
        profile = common_vars.__get_profile__()[1:-1][:-1]
        folder = common_vars.__get_s3_key__()[1:-1][:-1]
        sample_db_s3_folder = common_vars.__get_sample_db_s3_key__()[1:-1][:-1]
        bucket = common_vars.__get_s3_bucket__()[1:-1][:-1]
        vpc_id = network_inra_vars.__get_vpc_id__()[1:-1][:-1]
        security_group_id = network_inra_vars.__get_security_group_id__()[1:-1][:-1]
        tenant = common_vars.__get_tenant__()[1:-1][:-1]
        staging_env_prefix = common_vars.__get_staging_env_prefix__()[1:-1][:-1]
        db_subnet_group_name = database_infra_variables.__get_db_subnet_group_name__()[1:-1][:-1]
        rds_cluster_parameter_group_name = database_infra_variables.__get_rds_cluster_parame_group_name__()[1:-1][:-1]
        db_name = database_infra_variables.__get_db_name__()[1:-1][:-1]
        db_master_user = database_infra_variables.__get_db_master_user__()[1:-1][:-1]
        db_master_pwd = database_infra_variables.__get_db_master_pwd__()[1:-1][:-1]

        AwsProvider(self, "AWS", region=region, profile=profile)

        data_aws_vpc = DataAwsVpc(
            id=vpc_id,
            scope=scope,
            id_='data_aws_vpc'
        )
        # sg to be created for this stack purpose ie for db
        data_aws_security_group = DataAwsSecurityGroup(
            id=security_group_id,
            scope=scope,
            id_='data_aws_security_group'
        )

        data_aws_subnets_filter = DataAwsSubnetsFilter(
            name="vpc-id",
            values=[data_aws_vpc.id]
        )
        data_aws_subnets = DataAwsSubnets(
            filter=[data_aws_subnets_filter],
            scope=scope,
            id_='data_aws_subnets'
        )

        y = ",".join(map(str, data_aws_subnets.ids))
        # cat-dev to come as input from user as prefix either via tfvars or during module creation from template
        db_subnet_group_name = db_subnet_group_name + '-' + tenant + '-' + staging_env_prefix + '-dops-subnet-grp'
        db_subnet_group = DbSubnetGroup(
            name=db_subnet_group_name,
            subnet_ids=[y],
            scope=scope,
            id_="db_subnet_group"
        )

        # below configurations for cluster param group are not configurable hence hardcoded
        rds_logical_repl = RdsClusterParameterGroupParameter(
            name="rds.logical_replication",
            value="1",
            apply_method="pending-reboot"
        )
        wal_sender_timeout = RdsClusterParameterGroupParameter(
            name="wal_sender_timeout",
            value="0",
            apply_method="pending-reboot"
        )
        shared_preload_lib = RdsClusterParameterGroupParameter(
            name="shared_preload_libraries",
            value="pglogical",
            apply_method="pending-reboot"
        )
        rds_cluster_parameter_group_name = rds_cluster_parameter_group_name + '-' + tenant + '-' + staging_env_prefix + '-dops' \
                                                                                                                        '-rds-clus-param-grp'
        rds_cluster_parameter_group = RdsClusterParameterGroup(
            name=rds_cluster_parameter_group_name,
            family="aurora-postgresql15",
            parameter=[
                rds_logical_repl,
                wal_sender_timeout,
                shared_preload_lib
            ],
            scope=scope,
            id_="rds_cluster_parameter_group"
        )

        # only cluster identifier(dbname),user and pwd are configurable and should come as input from user others are
        # hardcoded,not configurable

        rds_cluster = RdsCluster(
            engine="aurora-postgresql",
            engine_mode="provisioned",
            engine_version="15.2",
            cluster_identifier=db_name,
            master_username=db_master_user,
            master_password=db_master_pwd,
            db_subnet_group_name=db_subnet_group.name,
            backup_retention_period=7,
            skip_final_snapshot=True,
            vpc_security_group_ids=[data_aws_security_group.id],
            db_cluster_parameter_group_name=rds_cluster_parameter_group.name,
            apply_immediately=True,
            scope=scope,
            id_="rds_cluster"
        )

        # instance class should be least cnfiguration for dev licence and hardcoded
        # instance class should come as an input from user based on documenation
        # dev team to prepare a simplified doc picking info  aws doc which maps data size to compute needed
        # QA to co-ordinate for testing and finding limits/quota/capacity for each compute

        rds_cluster_instance = RdsClusterInstance(
            identifier=db_name+"-instance-1",
            count=1,
            cluster_identifier=rds_cluster.cluster_identifier,
            instance_class="db.t3.medium",
            engine=rds_cluster.engine,
            engine_version=rds_cluster.engine_version,
            apply_immediately=True,
            scope=scope,
            id_="rds_cluster_instance"
        )

        # id_ should be change ,should you need to add another vpcendpoint host values not coming, so for now temp
        # get the details either from aws console or through some utlity command wrapper for aws cli
        TerraformOutput(self, "rds_aurora_postgres15_2_construct_output",
                        value=[
                            # rds_cluster.database_name,rds_cluster.connection.host,rds_cluster.connection.bastion_host
                            # ,rds_cluster_instance.endpoint
                            # ,rds_cluster_instance.connection.host
                            #    ,rds_cluster_instance.connection.bastion_host
                            #    ,rds_cluster_instance.connection.host_key
                            #    ,rds_cluster_instance.connection.proxy_host
                            #    ,rds_cluster_instance.connection.bastion_host_key
                            #    ,rds_cluster.connection.host_key
                            #    ,rds_cluster.connection.proxy_host
                            #    ,rds_cluster.connection.bastion_host_key
                        ]
                        )
        # bucket name should get generated during module creation and jinja template should be replaced by input from user
        # input should be cat-dev<customer or tenant name>-<environment>
        # region should also come as input from user during module creation
        # if difficult to templatize then pick from prop file or tfvars
        # if this construct/resource has already run previously for a tenant then
        # runnin the same for new tenants even with changed value will ask for
        # reinitialization of state which means 2 tenants cant have their own isolated states hence shared
        # check if there is a way to initialize a different s3 backend state in this scenario
        # for now proceed with some common bucket name
        # depending upon this state management and limitations from cdktf need to think of possible approached and
        # modularity for tenant isolation and accordingly decide the combination for constructs and stack
        # better way to handle multitenancy would be to create separate module for each tenant
        key = sample_db_s3_folder + "/terraform.tfstate"
        S3Backend(self,
                  bucket=bucket,
                  key=key,
                  encrypt=True,
                  region=region
                  )

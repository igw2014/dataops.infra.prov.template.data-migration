import argparse
import csv
import traceback
import boto3

from csx.core.data.migration.variables.DatabaseInfraVariables import DatabaseInfraVariables


class DatabaseServiceManager:
    rds_client = ''

    def __init__(self):
        self.rds_client = boto3.client('rds')

    def __get_db_details__(self, database_variable: DatabaseInfraVariables):

        db_name = database_variable.__get_db_name__()[1:-1][:-1]

        try:
            response = self.rds_client.describe_db_clusters(
                DBClusterIdentifier=db_name,
                MaxRecords=20,
                IncludeShared=False
            )

            print(response['DBClusters'][0]['Endpoint'])
        except Exception as e:
            print(e.__str__())

    def create_db_cluster_param_group(self,database_variable: DatabaseInfraVariables):
        db_param_grp_family = ''
        db_version_family = database_variable.__get_prod_db_version_family__()[1:-1][:-1]
        print(db_version_family)
        if db_version_family == '14':
            db_param_grp_family = 'aurora-postgresql14'
        if db_version_family == '15':
            db_param_grp_family = 'aurora-postgresql15'
        response = self.rds_client.create_db_cluster_parameter_group(
            DBClusterParameterGroupName='custom-aurora-postgres',
            DBParameterGroupFamily=db_param_grp_family,
            Description='custom-aurora-postgres',
            Tags=[
                {
                    'Key': 'rds.logical_replication',
                    'Value': '1'
                },
                {
                    'Key': 'wal_sender_timeout',
                    'Value': '0'
                },
                {
                    'Key': 'shared_preload_libraries',
                    'Value': 'pglogical'
                }
            ]
        )
        print('Sucessfully created custom DB Cluster Param Group Group')

    def modify_db_cluster_param_group(self,database_variable: DatabaseInfraVariables):
        db_param_grp_family = ''
        db_version_family = database_variable.__get_prod_db_version_family__()[1:-1][:-1]
        if db_version_family == '14':
            db_param_grp_family = 'aurora-postgresql14'
        if db_version_family == '15':
            db_param_grp_family = 'aurora-postgresql15'
        response = self.rds_client.modify_db_cluster_parameter_group(
            DBClusterParameterGroupName='custom-aurora-postgres',
            Parameters=[
                {
                    'ParameterName': 'rds.logical_replication',
                    'ParameterValue': '1',
                    'ApplyMethod': 'pending-reboot',
                },
                {
                    'ParameterName': 'wal_sender_timeout',
                    'ParameterValue': '0',
                    'ApplyMethod': 'pending-reboot',
                },
                {
                    'ParameterName': 'shared_preload_libraries',
                    'ParameterValue': 'pglogical',
                    'ApplyMethod': 'pending-reboot',
                }
            ]
        )
        print('Sucessfully updated custom DB Cluster Param Group Group')

    def modify_db_cluster(self, database_variable: DatabaseInfraVariables):
        print(database_variable.__get_prod_db_name__()[1:-1][:-1])
        response = self.rds_client.modify_db_cluster(
            DBClusterIdentifier=database_variable.__get_prod_db_name__()[1:-1][:-1],
            ApplyImmediately=True,
            DBClusterParameterGroupName='custom-aurora-postgres'
        )
        print('Sucessfully updated  DB Cluster with custom db cluster param group')

    def reboot_db_instance(self, database_variable: DatabaseInfraVariables):

        response = self.rds_client.reboot_db_instance(
            DBInstanceIdentifier=database_variable.__get_db_instance_id__()[1:-1][:-1],
            ForceFailover=False
        )
        print('Started Rebooting Database Instance.')

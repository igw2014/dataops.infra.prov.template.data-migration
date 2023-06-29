from cdktf import TerraformVariable
from constructs import Construct


class DMS3_4_7_InfraVariables:
    data_replication_engine_name = ''
    source_name = ''
    target_name = ''
    migration_type = ''
    data_replication_task_name = ''
    schema_name = ''
    table_name = ''

    def __init__(self, scope: Construct, project_vars: dict):
        self.data_replication_engine_name = project_vars["data_replication_engine_name"]
        self.source_name = project_vars["source_name"]
        self.target_name = project_vars["target_name"]
        self.migration_type = project_vars["migration_type"]
        self.data_replication_task_name = project_vars["data_replication_task_name"]
        self.schema_name = project_vars["schema_name"]
        self.table_name = project_vars["table_name"]

    def __get_data_replication_engine_name__(self):
        return self.data_replication_engine_name

    def __get_source_name__(self):
        return self.source_name

    def __get_target_name__(self):
        return self.target_name

    def __get_migration_type__(self):
        return self.migration_type

    def __get_data_replication_task_name__(self):
        return self.data_replication_task_name

    def __get_schema_name__(self):
        return self.schema_name

    def __get_table_name__(self):
        return self.table_name


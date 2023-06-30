from cdktf import TerraformVariable
from constructs import Construct


class DatabaseInfraVariables:
    db_subnet_group_name = ''
    rds_cluster_parame_group_name = ''
    db_name = ''
    db_master_user = ''
    db_master_pwd = ''
    server_name = ''

    def __init__(self, scope: Construct, project_vars: dict):

        # self.db_subnet_group_name = project_vars["db_subnet_group_name"]
        # self.rds_cluster_parame_group_name = project_vars["rds_cluster_parame_group_name"]
        self.db_name = project_vars["db_name"]
        self.db_master_user = project_vars["db_master_user"]
        self.db_master_pwd = project_vars["db_master_pwd"]
        self.server_name = project_vars["server_name"]

    # def __get_db_subnet_group_name__(self):
    #     return self.db_subnet_group_name
    #
    # def __get_rds_cluster_parame_group_name__(self):
    #     return self.rds_cluster_parame_group_name

    def __get_db_name__(self):
        return self.db_name

    def __get_db_master_user__(self):
        return self.db_master_user

    def __get_db_master_pwd__(self):
        return self.db_master_pwd

    def __get_server_name__(self):
        return self.server_name



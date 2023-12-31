from cdktf import TerraformVariable
from constructs import Construct


class DatabaseInfraVariables:
    # db_subnet_group_name = ''
    # rds_cluster_parame_group_name = ''
    db_name = ''
    db_master_user = ''
    db_master_pwd = ''
    # server_name = ''
    ssh_host = ''
    ssh_pkey_path = ''
    schema = ''
    default_db_name = 'postgres'
    db_server_url = ''
    db_instance_id = ''
    prod_db_name = ''
    proddb_master_user = ''
    proddb_master_pwd = ''
    proddb_server_url = ''
    prod_db_version_family = ''
    db_instance_server = ''

    def __init__(self, scope: Construct, project_vars: dict):
        # self.db_subnet_group_name = project_vars["db_subnet_group_name"]
        # self.rds_cluster_parame_group_name = project_vars["rds_cluster_parame_group_name"]
        self.db_name = project_vars["db_name"]
        self.db_master_user = project_vars["db_master_user"]
        self.db_master_pwd = project_vars["db_master_pwd"]
        # self.server_name = project_vars["server_name"]
        self.ssh_host = project_vars["ssh_host"]
        self.ssh_pkey_path = project_vars["ssh_pkey_path"]
        self.schema = project_vars["schema"]
        self.db_server_url = project_vars["db_server_url"]
        self.db_instance_id = project_vars["db_instance_id"]
        self.proddb_master_user = project_vars["proddb_master_user"]
        self.proddb_master_pwd = project_vars["proddb_master_pwd"]
        self.proddb_server_url = project_vars["proddb_server_url"]
        self.prod_db_name = project_vars["prod_db_name"]
        self.prod_db_version_family = project_vars["prod_db_version_family"]
        self.db_instance_server = project_vars["db_instance_server"]

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

    # def __get_server_name__(self):
    #     return self.server_name

    def __get_ssh_host__(self):
        return self.ssh_host

    def __get_ssh_pkey_path__(self):
        return self.ssh_pkey_path

    def __get_schema__(self):
        return self.schema

    def __get_default_db_name__(self):
        return self.default_db_name

    def __get_db_server_url__(self):
        return self.db_server_url

    def __get_prod_db_name__(self):
        return self.prod_db_name

    def __get_db_instance_id__(self):
        return self.db_instance_id

    def __get_prod_master_user__(self):
        return self.proddb_master_user

    def __get_prod_master_pwd__(self):
        return self.proddb_master_pwd

    def __get_prod_db_server_url__(self):
        return self.proddb_server_url

    def __get_prod_db_version_family__(self):
        return self.prod_db_version_family

    def __get_db_instance_server__(self):
        return self.db_instance_server


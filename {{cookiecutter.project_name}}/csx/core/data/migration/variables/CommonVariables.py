from cdktf import TerraformVariable
from constructs import Construct


class CommonVariables:
    region = ''
    profile = ''
    s3_bucket = ''
    s3_key = ''
    tenant = ''
    staging_env_prefix = ''
    sample_db_s3_key = ''


    def __init__(self, scope: Construct, project_vars: dict):
        # self.region = TerraformVariable(scope, "region",
        #                                 type="string",
        #                                 default="",
        #                                 description="AWS Region"
        #                                 )
        # self.profile = TerraformVariable(scope, "profile",
        #                                  type="string",
        #                                  default="",
        #                                  description="AWS profile"
        #                                  )
        # self.s3_bucket = TerraformVariable(scope, "s3_bucket",
        #                                    type="string",
        #                                    default="",
        #                                    description="s3_bucket"
        #                                    )
        # self.s3_key = TerraformVariable(scope, "s3_key",
        #                                 type="string",
        #                                 default="",
        #                                 description="s3_key"
        #                                 )
        self.region = project_vars["region"]
        self.profile = project_vars["profile"]
        self.s3_bucket = project_vars["s3_bucket"]
        self.s3_key = project_vars["s3_key"]
        self.tenant = project_vars["tenant"]
        self.staging_env_prefix = project_vars["staging_env_prefix"]
        self.sample_db_s3_key = project_vars["sample_db_s3_key"]


    def __get_region__(self):
        return self.region

    def __get_profile__(self):
        return self.profile

    def __get_s3_bucket__(self):
        return self.s3_bucket

    def __get_s3_key__(self):
        return self.s3_key

    def __get_tenant__(self):
        return self.tenant

    def __get_staging_env_prefix__(self):
        return self.staging_env_prefix

    def __get_sample_db_s3_key__(self):
        return self.sample_db_s3_key



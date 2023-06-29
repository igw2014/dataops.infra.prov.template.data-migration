from cdktf import TerraformVariable
from constructs import Construct


class NetworkInfraVariables:
    security_group_id = ''
    dms_security_group_id = ''
    cidr_blocks = ''
    vpc_id = ''
    def __init__(self, scope: Construct, project_vars: dict):
        # self.security_group_id = TerraformVariable(scope, "security_group_id",
        #                                 type="string",
        #                                 default="",
        #                                 description="security_group_id"
        #                                 )
        # # self.security_group_id = "sg-0a5c295002222de0c"
        # self.cidr_blocks = TerraformVariable(scope, "cidr_blocks",
        #                                  type="string",
        #                                  default="",
        #                                  description="cidr_blocks"
        #                                  )
        self.security_group_id = project_vars["security_group_id"]
        self.cidr_blocks = project_vars["cidr_blocks"]
        self.vpc_id = project_vars["vpc_id"]
        self.dms_security_group_id = project_vars["dms_security_group_id"]

    def __get_security_group_id__(self):
        return self.security_group_id

    def __get_cidr_blocks__(self):
        return self.cidr_blocks

    def __get_vpc_id__(self):
        return self.vpc_id

    def __get_dms_security_group_id__(self):
        return self.dms_security_group_id

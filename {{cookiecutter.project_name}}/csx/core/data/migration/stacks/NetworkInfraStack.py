from cdktf import TerraformStack
from constructs import Construct
from csx.core.data.migration.constructs.VPCEndpointConstruct import VPCEndpointConstruct
from csx.core.data.migration.constructs.SecurityGroupRuleConstruct import SecurityGroupRuleConstruct
from csx.core.data.migration.variables.CommonVariables import CommonVariables
from csx.core.data.migration.variables.NetworkInfraVariables import NetworkInfraVariables


class NetworkInfraStack(TerraformStack):

    def __init__(self, scope: Construct, id: str,project_vars: dict):
        super().__init__(scope, id)

        # define resources here
        # VPCEndpointConstruct(self, "vpc-endpoint-construct")
        commmon_variables =  CommonVariables(scope,project_vars)
        network_variables = NetworkInfraVariables(scope,project_vars)

        SecurityGroupRuleConstruct(self,"sec-grp-rule-construct"
                                   ,commmon_variables
                                   ,network_variables
                                   )
        # SecurityGroupRuleConstruct(self, "sec-grp-rule-construct",project_vars)
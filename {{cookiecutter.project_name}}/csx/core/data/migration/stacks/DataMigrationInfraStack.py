from cdktf import TerraformStack
from constructs import Construct
from csx.core.data.migration.constructs.DMS3_4_7Construct import DMS3_4_7Construct
from csx.core.data.migration.variables.CommonVariables import CommonVariables
from csx.core.data.migration.variables.DatabaseInfraVariables import DatabaseInfraVariables
from csx.core.data.migration.variables.NetworkInfraVariables import NetworkInfraVariables
from csx.core.data.migration.variables.DMS3_4_7_InfraVariables import DMS3_4_7_InfraVariables


class DataMigrationInfraStack(TerraformStack):

    def __init__(self, scope: Construct, id: str,project_vars:dict):
        super().__init__(scope, id)

        # define resources here
        common_variables = CommonVariables(scope, project_vars)
        network_infra_variables = NetworkInfraVariables(scope, project_vars)
        database_infra_variables = DatabaseInfraVariables(scope, project_vars)
        dms_3_4_7_infra_variables = DMS3_4_7_InfraVariables(scope, project_vars)
        DMS3_4_7Construct(self, "dms-3.4.7-construct"
                          ,common_variables
                          ,network_infra_variables
                          ,dms_3_4_7_infra_variables
                          ,database_infra_variables)
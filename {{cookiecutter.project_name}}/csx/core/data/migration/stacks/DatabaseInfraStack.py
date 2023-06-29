from cdktf import TerraformStack
from constructs import Construct

from csx.core.data.migration.constructs.RDSAuroraPostgresSql_15_2_Construct import RDSAuroraPostgresSql_15_2_Construct
from csx.core.data.migration.variables.CommonVariables import CommonVariables
from csx.core.data.migration.variables.DatabaseInfraVariables import DatabaseInfraVariables
from csx.core.data.migration.variables.NetworkInfraVariables import NetworkInfraVariables


class DatabaseInfraStack(TerraformStack):

    def __init__(self, scope: Construct, id: str,project_vars: dict):
        super().__init__(scope, id)

        # define resources here
        common_variables = CommonVariables(scope, project_vars)
        network_infra_variables = NetworkInfraVariables(scope,project_vars)
        database_infra_variables = DatabaseInfraVariables(scope,project_vars)
        RDSAuroraPostgresSql_15_2_Construct(self, "rds-aurora-postgres14-construct"
                                            ,common_variables
                                            ,network_infra_variables
                                            ,database_infra_variables)
#!/usr/bin/env python
from cdktf import App
from csx.core.data.migration.stacks.NetworkInfraStack import NetworkInfraStack
from csx.core.data.migration.stacks.DatabaseInfraStack import DatabaseInfraStack
from csx.core.data.migration.stacks.DataMigrationInfraStack import DataMigrationInfraStack

#To-Do:How to include only necessary terraform module sin cdktf.json.Not working currently due to some terraform modules
#not being found in terraform module repo. This is to ensure less size of module
# //    "terraform-aws-modules/vpc",
# //    "terraform-aws-modules/iam",-->Not found
# //    "terraform-aws-modules/security-group",
# //    "terraform-aws-modules/s3-bucket",
# //    "terraform-aws-modules/rds",
# //    "terraform-aws-modules/rds-aurora",-->Not found
# //    "terraform-aws-modules/dms"
project_vars = {}
with open("staging.auto.tfvars") as staging_file:
    for line in staging_file:
        name, var = line.partition("=")[::2]
        project_vars[name.strip()] = str(var)
app = App()
NetworkInfraStack(app, "network-infra-stack",project_vars)
DatabaseInfraStack(app,"database-infra-stack",project_vars)
DataMigrationInfraStack(app,"data-migration-infra-stack",project_vars)
app.synth()

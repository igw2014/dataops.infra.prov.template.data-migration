import argparse
import csv
import traceback
from cdktf import App
from csx.core.data.migration.utity.postgres_client import PostgresqlClient
from csx.core.data.migration.service.management.NetworkServiceManager import NetworkServiceManager
from csx.core.data.migration.variables.DatabaseInfraVariables import DatabaseInfraVariables
from csx.core.data.migration.variables.NetworkInfraVariables import NetworkInfraVariables

if __name__ == "__main__":
    postgres_client = PostgresqlClient()
    network_service_manager = NetworkServiceManager()

    app = App()

    argParser = argparse.ArgumentParser()
    argParser.add_argument("-c", "--command", help="command")
    # argParser.add_argument("-s", "--secgrp-id", help="sample db security frp id")
    # argParser.add_argument("-i", "--ec2-private-ip", help="ec2 instance private ip")
    args = argParser.parse_args()
    # print("args=%s" % args)

    print("args.command=%s" % args.command)
    # print("args.secgrp_id=%s" % args.secgrp_id)
    # print("args.ec2_private_ip=%s" % args.ec2_private_ip)
    project_vars = {}
    with open("{{ cookiecutter.environment }}.tfvars") as tfvar_file:
        for line in tfvar_file:
            name, var = line.partition("=")[::2]
            project_vars[name.strip()] = str(var)

    network_variables = NetworkInfraVariables(app, project_vars)
    database_infra_variables = DatabaseInfraVariables(app, project_vars)

    # sample_db_security_group_id = project_vars['sample_db_security_group_id']
    # ec2_private_ip = project_vars['ec2_private_ip']

    command = args.command

    match command:
        case "allow-db-access":
            network_service_manager.__add_security_group_rule_to_db__(network_variables)
        case "create-sample-schema":
            postgres_client.__grant_all_permission__(database_infra_variables)
            postgres_client.__create_database__(database_infra_variables)
            postgres_client.__show_databases__(database_infra_variables)
            postgres_client.__create_schema__(database_infra_variables)
            postgres_client.__create_tables__(database_infra_variables)
        case "install-db-extensions":
            postgres_client.__create_extension__(database_infra_variables)
        case "load-sample-data":
            postgres_client.__load_tables__(database_infra_variables)
        case _:
            print("Matching Command Not Found.")

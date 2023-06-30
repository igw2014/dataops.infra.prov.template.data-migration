import argparse
import csv
import traceback
from csx.core.data.migration.utity.postgres_client import PostgresqlClient
from csx.core.data.migration.service.management.NetworkServiceManager import NetworkServiceManager

if __name__ == "__main__":
    postgres_client = PostgresqlClient()
    network_service_manager = NetworkServiceManager()
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

    sample_db_security_group_id = project_vars['sample_db_security_group_id']
    ec2_private_ip = project_vars['ec2_private_ip']

    command = args.command

    match command:
        case "allow-db-access":
            network_service_manager.__add_security_group_rule_to_db__(sample_db_security_group_id, ec2_private_ip)
        case "create-sample-schema":
            postgres_client.__grant_all_permission__("postgres"
                                 , project_vars['ssh_host']
                                 , project_vars['ssh_pkey_path']
                                 , project_vars['server_name']
                                 , project_vars['db_master_user']
                                 , project_vars['db_master_pwd'])
            postgres_client.__create_database__(project_vars['db_name']
                                 , project_vars['ssh_host']
                                 , project_vars['ssh_pkey_path']
                                 , project_vars['server_name']
                                 , project_vars['db_master_user']
                                 , project_vars['db_master_pwd']
                                 , "postgres")
            postgres_client.__show_databases__("postgres"
                                 , project_vars['ssh_host']
                                 , project_vars['ssh_pkey_path']
                                 , project_vars['server_name']
                                 , project_vars['db_master_user']
                                 , project_vars['db_master_pwd'])
            postgres_client.__create_schema__(project_vars['db_name']
                                 , project_vars['ssh_host']
                                 , project_vars['ssh_pkey_path']
                                 , project_vars['server_name']
                                 , project_vars['db_master_user']
                                 , project_vars['db_master_pwd']
                                 , project_vars['schema'])
            postgres_client.__create_tables__(project_vars['db_name']
                                 , project_vars['ssh_host']
                                 , project_vars['ssh_pkey_path']
                                 , project_vars['server_name']
                                 , project_vars['db_master_user']
                                 , project_vars['db_master_pwd'])
        case "install-db-extensions":
            postgres_client.__create_extension__(project_vars['db_name']
                                 , project_vars['ssh_host']
                                 , project_vars['ssh_pkey_path']
                                 , project_vars['server_name']
                                 , project_vars['db_master_user']
                                 , project_vars['db_master_pwd'])
        case "load-sample-data":
            postgres_client.__load_tables__(project_vars['db_name']
                                 , project_vars['ssh_host']
                                 , project_vars['ssh_pkey_path']
                                 , project_vars['server_name']
                                 , project_vars['db_master_user']
                                 , project_vars['db_master_pwd']
                                 , project_vars['schema'])
        case _:
            print("Matching Command Not Found.")

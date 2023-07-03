import argparse
import csv
import os
import traceback

import psycopg2
from psycopg2 import sql
from sshtunnel import SSHTunnelForwarder
from csx.core.data.migration.variables.DatabaseInfraVariables import DatabaseInfraVariables


class PostgresqlClient:
    def __connect_postgres__(self, database_name: str
                             , ssh_host: str
                             , ssh_pkey_path: str
                             , db_server_url: str
                             , db_user: str
                             , db_pwd: str):
        conn = ''
        try:
            # print('Connecting to the PostgreSQL Database...')
            # print(database_name)
            # print(ssh_host)
            # print(ssh_pkey_path)
            # print(db_server_url)
            # print(db_user)
            # print(db_pwd)

            sshtunnel = SSHTunnelForwarder(
                ssh_address_or_host=ssh_host,
                ssh_username='ec2-user',
                ssh_pkey=ssh_pkey_path,
                remote_bind_address=(db_server_url, 5432)
            )
            sshtunnel.start()
            print("****SSH Tunnel Established****")

            conn = psycopg2.connect(
                user=db_user,
                password=db_pwd,
                host="localhost",
                port=sshtunnel.local_bind_port,
                database=database_name
            )

            print("Connected to PostgreSQL Database...")
        except Exception as e:
            print('Connection Has Failed...')
            print(e.__str__())
        return conn

    def __grant_all_permission__(self, db_infra_vars:DatabaseInfraVariables):
        global cursor, conn
        try:
            default_db_name = db_infra_vars.__get_default_db_name__()
            ssh_host = db_infra_vars.__get_ssh_host__()[1:-1][:-1]
            ssh_pkey_path = db_infra_vars.__get_ssh_pkey_path__()[1:-1][:-1]
            db_server_url = db_infra_vars.__get_db_server_url__()[1:-1][:-1]
            db_user = db_infra_vars.__get_db_master_user__()[1:-1][:-1]
            db_pwd = db_infra_vars.__get_db_master_pwd__()[1:-1][:-1]
            conn = self.__connect_postgres__(default_db_name
                                             , ssh_host
                                             , ssh_pkey_path
                                             , db_server_url
                                             , db_user
                                             , db_pwd)
            cursor = conn.cursor()
            conn.autocommit = True  # !
            print("Creating Permissions in DB........")
            grant_cmd = sql.SQL('ALTER TABLESPACE pg_default OWNER TO {}'.format(db_user))
            cursor.execute(grant_cmd)
            print("Permission Creation Successfull")
        except Exception as e:
            conn.rollback()
            print(e.__str__())
            tb = traceback.format_exc()
            print(tb)
        finally:
            cursor.close()
            conn.close()

    def __create_database__(self, db_infra_vars:DatabaseInfraVariables):
        global cursor, conn
        try:
            default_db_name = db_infra_vars.__get_default_db_name__()
            db_name = db_infra_vars.__get_db_name__()[1:-1][:-1]
            ssh_host = db_infra_vars.__get_ssh_host__()[1:-1][:-1]
            ssh_pkey_path = db_infra_vars.__get_ssh_pkey_path__()[1:-1][:-1]
            db_server_url = db_infra_vars.__get_db_server_url__()[1:-1][:-1]
            db_user = db_infra_vars.__get_db_master_user__()[1:-1][:-1]
            db_pwd = db_infra_vars.__get_db_master_pwd__()[1:-1][:-1]
            conn = self.__connect_postgres__(default_db_name
                                             , ssh_host
                                             , ssh_pkey_path
                                             , db_server_url
                                             , db_user
                                             , db_pwd)
            cursor = conn.cursor()
            conn.autocommit = True  # !
            print("Creating Database........")
            dbname = sql.Identifier(db_name)
            create_cmd = sql.SQL('CREATE DATABASE {} tablespace pg_default').format(dbname)
            grant_cmd = sql.SQL('GRANT ALL PRIVILEGES ON DATABASE {} TO {}'.format(db_name, db_user))
            cursor.execute(create_cmd)
            cursor.execute(grant_cmd)
            print("Database Creation Successfull")
        except Exception as e:
            conn.rollback()
            print(e.__str__())
            tb = traceback.format_exc()
            print(tb)
        finally:
            cursor.close()
            conn.close()

    def __create_schema__(self, db_infra_vars: DatabaseInfraVariables):
        global conn
        try:
            schema = db_infra_vars.__get_schema__()[1:-1][:-1]
            db_name = db_infra_vars.__get_db_name__()[1:-1][:-1]
            ssh_host = db_infra_vars.__get_ssh_host__()[1:-1][:-1]
            ssh_pkey_path = db_infra_vars.__get_ssh_pkey_path__()[1:-1][:-1]
            db_server_url = db_infra_vars.__get_db_server_url__()[1:-1][:-1]
            db_user = db_infra_vars.__get_db_master_user__()[1:-1][:-1]
            db_pwd = db_infra_vars.__get_db_master_pwd__()[1:-1][:-1]
            conn = self.__connect_postgres__(db_name
                                             , ssh_host
                                             , ssh_pkey_path
                                             , db_server_url
                                             , db_user
                                             , db_pwd)
            conn.autocommit = True  # !
            print("Creating Schema for DB...")
            s = f"CREATE SCHEMA {schema} AUTHORIZATION {db_user};"

            # Print all the databases
            try:
                with conn.cursor() as cur:
                    cur.execute(s)
            except Exception as e:
                print(e.__str__())
                tb = traceback.format_exc()
                print(tb)
            finally:
                cur.close()
            print("Completed creating schema for DB...")
            print("--------------------------------")

            # Now get the data in table test
        except Exception as e:

            print(e.__str__())
            tb = traceback.format_exc()
            print(tb)
        finally:
            conn.close()

    def __create_extension__(self, db_infra_vars: DatabaseInfraVariables):
        global conn
        try:

            db_name = db_infra_vars.__get_db_name__()[1:-1][:-1]
            ssh_host = db_infra_vars.__get_ssh_host__()[1:-1][:-1]
            ssh_pkey_path = db_infra_vars.__get_ssh_pkey_path__()[1:-1][:-1]
            db_server_url = db_infra_vars.__get_db_server_url__()[1:-1][:-1]
            db_user = db_infra_vars.__get_db_master_user__()[1:-1][:-1]
            db_pwd = db_infra_vars.__get_db_master_pwd__()[1:-1][:-1]

            conn = self.__connect_postgres__(db_name
                                             , ssh_host
                                             , ssh_pkey_path
                                             , db_server_url
                                             , db_user
                                             , db_pwd)
            conn.autocommit = True  # !
            print("Creating extension for DB...")
            s = f"create extension pglogical;"

            # Print all the databases
            try:
                with conn.cursor() as cur:
                    cur.execute(s)
            except Exception as e:
                print(e.__str__())
                tb = traceback.format_exc()
                print(tb)
            finally:
                cur.close()
            print("Completed creating extension for DB...")
            print("--------------------------------")

            # Now get the data in table test
        except Exception as e:

            print(e.__str__())
            tb = traceback.format_exc()
            print(tb)
        finally:
            conn.close()

    def __create_tables__(self, db_infra_vars:DatabaseInfraVariables):
        global conn
        try:
            db_name = db_infra_vars.__get_db_name__()[1:-1][:-1]
            ssh_host = db_infra_vars.__get_ssh_host__()[1:-1][:-1]
            ssh_pkey_path = db_infra_vars.__get_ssh_pkey_path__()[1:-1][:-1]
            db_server_url = db_infra_vars.__get_db_server_url__()[1:-1][:-1]
            db_user = db_infra_vars.__get_db_master_user__()[1:-1][:-1]
            db_pwd = db_infra_vars.__get_db_master_pwd__()[1:-1][:-1]

            conn = self.__connect_postgres__(db_name
                                             , ssh_host
                                             , ssh_pkey_path
                                             , db_server_url
                                             , db_user
                                             , db_pwd)
            conn.autocommit = True  # !
            print("Creating Tables for DB...")

            # Print all the databases
            file_dir = os.path.dirname(os.path.realpath('__file__'))
            # print(file_dir)

            try:
                with conn.cursor() as cur:
                    cur.execute(open(file_dir+"/csx/core/data/migration/sample/schema/schema.sql", "r").read())
            except Exception as e:
                print(e.__str__())
                tb = traceback.format_exc()
                print(tb)
            finally:
                cur.close()
            print("Completed Tables schema for DB...")
            print("--------------------------------")

            # Now get the data in table test
        except Exception as e:

            print(e.__str__())
            tb = traceback.format_exc()
            print(tb)
        finally:
            conn.close()

    def __load_tables__(self, db_infra_vars: DatabaseInfraVariables):
        global conn
        try:
            db_name = db_infra_vars.__get_db_name__()[1:-1][:-1]
            ssh_host = db_infra_vars.__get_ssh_host__()[1:-1][:-1]
            ssh_pkey_path = db_infra_vars.__get_ssh_pkey_path__()[1:-1][:-1]
            db_server_url = db_infra_vars.__get_db_server_url__()[1:-1][:-1]
            db_user = db_infra_vars.__get_db_master_user__()[1:-1][:-1]
            db_pwd = db_infra_vars.__get_db_master_pwd__()[1:-1][:-1]
            schema = db_infra_vars.__get_schema__()[1:-1][:-1]
            conn = self.__connect_postgres__(db_name
                                             , ssh_host
                                             , ssh_pkey_path
                                             , db_server_url
                                             , db_user
                                             , db_pwd)
            conn.autocommit = True  # !
            print("Loading Data into Tables from CSV File...")

            # Print all the databases
            cur = conn.cursor()
            schema = schema+'.country'
            try:
                # remove hardcoded schema accept from argument
                f = open('csx/core/data/migration/sample/data/country_202305191429.csv', "r")
                cur.execute("Truncate {} Cascade;".format(schema))
                cur.copy_expert("copy {} from STDIN CSV HEADER QUOTE '\"'".format(schema), f)
            except Exception as e:
                print(e.__str__())
                tb = traceback.format_exc()
                print(tb)
            finally:
                cur.close()
            print("Completed Loading Tables ...")
            print("--------------------------------")

            # Now get the data in table test
        except Exception as e:

            print(e.__str__())
            tb = traceback.format_exc()
            print(tb)
        finally:
            conn.close()

    def __show_databases__(self, db_infra_vars: DatabaseInfraVariables):
        global conn
        try:
            db_name = db_infra_vars.__get_db_name__()[1:-1][:-1]
            ssh_host = db_infra_vars.__get_ssh_host__()[1:-1][:-1]
            ssh_pkey_path = db_infra_vars.__get_ssh_pkey_path__()[1:-1][:-1]
            db_server_url = db_infra_vars.__get_db_server_url__()[1:-1][:-1]
            db_user = db_infra_vars.__get_db_master_user__()[1:-1][:-1]
            db_pwd = db_infra_vars.__get_db_master_pwd__()[1:-1][:-1]
            conn = self.__connect_postgres__(db_name
                                             , ssh_host
                                             , ssh_pkey_path
                                             , db_server_url
                                             , db_user
                                             , db_pwd)
            conn.autocommit = True  # !
            print("Getting data from the catalog")
            s = "select datname from pg_catalog.pg_database;"

            # Print all the databases
            try:
                with conn.cursor() as cur:
                    cur.execute(s)
                    for r in cur:
                        print(r)
            except Exception as e:
                print(e.__str__())
            finally:
                cur.close()
            print("--------------------------------")

            # Now get the data in table test
        except Exception as e:

            print(e.__str__())
            tb = traceback.format_exc()
            print(tb)
        finally:
            conn.close()

if __name__ == "__main__":
    db_name = 'postgres'
    ssh_host = '3.236.183.225'
    pkey_path = '/Users/akshaytigga/Downloads/catdevdopsec2kp1.pem'
    user = 'salesadmin'
    pwd = 'salesadmin'
    server_url = 'salesdev.cluster-cefcmch6dncq.us-east-1.rds.amazonaws.com'
    client = PostgresqlClient()

    client.__connect_postgres__(db_name,ssh_host,pkey_path,server_url,user,pwd)
#     # user = "jcbdevadmin"
#     # dbname = "jcbdevdb"
#     # schema_name = "jcbdevschema"
#     argParser = argparse.ArgumentParser()
#     argParser.add_argument("-u", "--user", help="user name")
#     argParser.add_argument("-d", "--dbname", help="db name")
#     argParser.add_argument("-s", "--schema", help="schema name")
#     args = argParser.parse_args()
#     print("args=%s" % args)
#
#     print("args.user=%s" % args.user)
#     print("args.dbname=%s" % args.dbname)
#     print("args.schema=%s" % args.schema)
#     #add arguments for ec3 host,db host,key path,user,pwd
#     grant_all_permission('postgres', args.user)
#     create_database('postgres', args.dbname, args.user)
#     show_databases('postgres')
#     create_schema(args.dbname, args.schema, args.user)
#     create_extension(args.dbname)
#     create_tables(args.dbname)
#     load_tables(args.dbname)

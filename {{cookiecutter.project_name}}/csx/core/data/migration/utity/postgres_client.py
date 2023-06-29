import argparse
import csv
import traceback

import psycopg2
from psycopg2 import sql
from sshtunnel import SSHTunnelForwarder


def connect_postgres(database_name):
    conn = ''
    try:
        print('Connecting to the PostgreSQL Database...')
        sshtunnel = SSHTunnelForwarder(
            ssh_address_or_host='ec2-3-82-190-249.compute-1.amazonaws.com',
            ssh_username='ec2-user',
            ssh_pkey='/Users/akshaytigga/Downloads/tatadevinstance.pem',
            remote_bind_address=('jcbdevdb.cluster-cefcmch6dncq.us-east-1.rds.amazonaws.com', 5432)
        )
        sshtunnel.start()
        print("****SSH Tunnel Established****")

        conn = psycopg2.connect(
            user="jcbdevadmin",
            password="jcbdevadmin",
            host="localhost",
            port=sshtunnel.local_bind_port,
            database=database_name
        )

        print("Connected to PostgreSQL Database...")
    except Exception as e:
        print('Connection Has Failed...')
        print(e.__str__())
    return conn

def grant_all_permission(db_name, dbuser):
    global cursor, conn
    try:

        conn = connect_postgres(db_name)
        cursor = conn.cursor()
        conn.autocommit = True  # !
        print("Creating Database........")
        grant_cmd = sql.SQL('ALTER TABLESPACE pg_default OWNER TO {}'.format(dbuser))
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


def create_database(db_name, name, dbuser):
    global cursor, conn
    try:

        conn = connect_postgres(db_name)
        cursor = conn.cursor()
        conn.autocommit = True  # !
        print("Creating Database........")
        dbname = sql.Identifier(name)
        create_cmd = sql.SQL('CREATE DATABASE {} tablespace pg_default').format(dbname)
        grant_cmd = sql.SQL('GRANT ALL PRIVILEGES ON DATABASE {} TO {}'.format(name, dbuser))
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


def create_schema(db_name, schema, dbuser):
    global conn
    try:
        conn = connect_postgres(db_name)
        conn.autocommit = True  # !
        print("Creating Schema for DB...")
        s = f"CREATE SCHEMA {schema} AUTHORIZATION {dbuser};"

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

def create_extension(db_name):
    global conn
    try:
        conn = connect_postgres(db_name)
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


def create_tables(db_name):
    global conn
    try:
        conn = connect_postgres(db_name)
        conn.autocommit = True  # !
        print("Creating Tables for DB...")

        # Print all the databases
        try:
            with conn.cursor() as cur:
                cur.execute(open("csx/core/data/migration/source/sample/schema/schema.sql", "r").read())
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


def load_tables(db_name):
    global conn
    try:
        conn = connect_postgres(db_name)
        conn.autocommit = True  # !
        print("Loading Data into Tables from CSV File...")

        # Print all the databases
        cur = conn.cursor()
        try:
            # remove hardcoded schema accept from argument
            f = open('/Users/akshaytigga/country_202305191429.csv', "r")
            cur.execute("Truncate {} Cascade;".format('jcbdevschema.country'))
            cur.copy_expert("copy {} from STDIN CSV HEADER QUOTE '\"'".format('jcbdevschema.country'), f)
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



def show_databases(db_name):
    global conn
    try:
        conn = connect_postgres(db_name)
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
    # user = "jcbdevadmin"
    # dbname = "jcbdevdb"
    # schema_name = "jcbdevschema"
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-u", "--user", help="user name")
    argParser.add_argument("-d", "--dbname", help="db name")
    argParser.add_argument("-s", "--schema", help="schema name")
    args = argParser.parse_args()
    print("args=%s" % args)

    print("args.user=%s" % args.user)
    print("args.dbname=%s" % args.dbname)
    print("args.schema=%s" % args.schema)
    #add arguments for ec3 host,db host,key path,user,pwd
    grant_all_permission('postgres', args.user)
    create_database('postgres', args.dbname, args.user)
    show_databases('postgres')
    create_schema(args.dbname, args.schema, args.user)
    create_extension(args.dbname)
    create_tables(args.dbname)
    load_tables(args.dbname)

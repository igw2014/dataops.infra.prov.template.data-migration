#Common Variables
region="us-east-1"
profile="default"
tf_state_s3_bucket="-dops-tf-state"
data_migration_s3_key="data-migration"
sample_db_s3_key="sample-database"
tenant="{{ cookiecutter.tenant_name }}"
env_prefix="{{ cookiecutter.environment }}"
# Network Infra Variables
vpc_id="vpc-0d40cf14ef5b2f1c0"
sample_db_security_group_id="sg-0eb3e016ebdd16410"
dms_security_group_id="sg-09fd7e8513477732f"
ec2_private_ip="10.0.1.35"
ssh_host="3.236.183.225"
ssh_pkey_path="/Users/akshaytigga/.ssh/catdevdopsec2kp1.pem"
cidr_blocks="[10.0.1.35/24]"
# Sample Database Infra Variables
db_name="salesdev"
schema="homeequipments"
db_master_user="salesadmin"
db_master_pwd="salesadmin"
server_name=""
db_server_url="salesdev.cluster-cefcmch6dncq.us-east-1.rds.amazonaws.com"
# DMS 3.4.7 Infra Variables
data_replication_engine_name="test"
source_name="test"
target_name="test"
migration_type="0"
data_replication_task_name="test"
schema_name="test"
table_name="homeequipments"
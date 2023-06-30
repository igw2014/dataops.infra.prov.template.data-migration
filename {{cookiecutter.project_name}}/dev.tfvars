#Common Variables
region="us-east-1"
profile="default"
s3_bucket="-dops-tf-state"
s3_key="data-migration"
sample_db_s3_key="sample-database"
tenant="{{ cookiecutter.tenant_name }}"
env_prefix={{ cookiecutter.environment }}
# Network Infra Variables
security_group_id="sg-0a80203a1294775d1"
dms_security_group_id=""
cidr_blocks="172.31.82.204/32"
vpc_id="vpc-0f1173895f32ddf98"
# Sample Database Infra Variables
db_subnet_group_name="test"
rds_cluster_parame_group_name="test"
db_name="sales"
db_master_user="salesadmin"
db_master_pwd="salesadmin"
server_name=""
# DMS 3.4.7 Infra Variables
data_replication_engine_name="test"
source_name="test"
target_name="test"
migration_type="0"
data_replication_task_name="test"
schema_name="test"
table_name="country"
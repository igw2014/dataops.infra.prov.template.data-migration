import argparse
import csv
import traceback
import boto3

from csx.core.data.migration.variables.NetworkInfraVariables import NetworkInfraVariables


class NetworkServiceManager:

    def __add_security_group_rule_to_db__(self, network_variables:NetworkInfraVariables):

        security_group_id = network_variables.__get_sample_db_security_group_id__()[1:-1][:-1]
        ec2_private_ip = network_variables.__get_ec2_private_ip__()[1:-1][:-1]
        port_range_start = 5432
        protocol = "tcp"
        cidr = ec2_private_ip + "/32"
        description = "security_group_rule_to_db from ec2 tunnel"

        ec2 = boto3.resource('ec2')
        security_group = ec2.SecurityGroup(security_group_id)
        try:
            security_group.authorize_ingress(
                DryRun=False,
                IpPermissions=[
                    {
                        'FromPort': port_range_start,
                        'ToPort': 5432,
                        'IpProtocol': protocol,
                        'IpRanges': [
                            {
                                'CidrIp': cidr,
                                'Description': description
                            },
                        ]
                    }
                ]
            )
        except Exception as e:
            print(e.__str__())
        finally:
            print("Permission for EC2 Tunnel to Access Sample DB Granted")

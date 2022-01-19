import boto3
from botocore.exceptions import ClientError


class Ec2:
    def __init__(self, instance_id):
        self.instance_id = instance_id
        self.ec2 = boto3.client('ec2')

    def describe_instance(self):
        response = self.ec2.describe_instances()
        return response

    def start_instance(self):
        try:
            self.ec2.start_instances(
                InstanceIds=[self.instance_id], DryRun=True)

        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        try:
            response = self.ec2.start_instances(
                InstanceIds=[self.instance_id], DryRun=False)
            print(response)
        except ClientError as e:
            print(e)

    def get_instance_status_code(self):
        response = self.ec2.describe_instance_status(
            InstanceIds=[self.instance_id])
        statuses = response.get("InstanceStatuses")

        if len(statuses) > 0:
            return statuses[0].get("InstanceState").get("Code")
        else:
            return None

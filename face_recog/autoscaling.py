import boto3
import time

ec2 = boto3.client('ec2')
cloudwatch = boto3.client('cloudwatch')

CPU_UPPER_THRESHOLD = 70
CPU_LOWER_THRESHOLD = 20
MIN_INSTANCES = 0
MAX_INSTANCES = 20
REQUEST_QUEUE_URL = ""



def main():
    while True:
        queue_length = get_queue_length(REQUEST_QUEUE_URL)
        print("SQS Request Queue Length is : " + queue_length)

        response = ec2.describe_instances(
            Filters=[{'Name': '' , 'Values' : 'Running'}]
        )

        current_instance_length = len()
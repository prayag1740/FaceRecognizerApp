import boto3, time, json

ec2_client = boto3.client('ec2')
sqs_client = boto3.client('sqs')

AMI_ID = "ami-0b81f4988e1494c27"
INSTANCE_TYPE= "t2.micro"
MIN_INSTANCES = 0
MAX_INSTANCES = 20
SCALE_IN_THRESHOLD = 1
SCALE_OUT_THRESHOLD = 3
SECURITY_GROUP = ['sg-092d7173df0cd797b']

REQUEST_SQS_URL = 'https://sqs.us-east-1.amazonaws.com/637423519415/1227975517-req-queue'

user_data_script = '''#!/bin/bash  
python3 /home/ec2-user/FaceRecognizerDL/face_recognition.py > logs.log
'''


def get_queue_length():

    response = sqs_client.get_queue_attributes(QueueUrl=REQUEST_SQS_URL, AttributeNames=['ApproximateNumberOfMessages'])
    return int(response['Attributes']['ApproximateNumberOfMessages'])


def start_instance(instance_name):
    response = ec2_client.run_instances(
        ImageId=AMI_ID,
        InstanceType=INSTANCE_TYPE,
        SecurityGroupIds=SECURITY_GROUP,
        MinCount=1,
        MaxCount=1,
        KeyName='prayag_ec2_keyPair4',
        UserData=user_data_script,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': instance_name
                    }
                ]
            }
        ]
    )
    return response['Instances'][0]['InstanceId']


def stop_instance(instance_id):
    ec2_client.terminate_instances(InstanceIds=[instance_id])


def get_running_instances():
    response = ec2_client.describe_instances(Filters=[
        {
            'Name' : 'image-id',
            'Values' : [AMI_ID]
        },
        {
            'Name' : 'instance-state-name',
            'Values' : ['running']
        }
    ])
    instance_data = response['Reservations']
    return instance_data


def get_instance_id_for_scale_in(instance_data):
    instance_data = instance_data[0]
    instance_id = instance_data['Instances'][0]['InstanceId']
    return instance_id


 

def main():
    while True:
        queue_length = get_queue_length()
        
        print("SQS Request Queue Length is : " + str(queue_length))

        running_instances = get_running_instances()
        running_instance_count = len(running_instances)
        print("Running instances count is : " + str(running_instance_count))

        #first time instance initiate
        if running_instance_count == 0 and queue_length > 0:
            print("Starting instance for the first time")
            instance_count = str(running_instance_count+1)
            instance_name = f"app-tier-instance-{instance_count}"
            instance_id = start_instance(instance_name)
            print(f"instance with id {instance_id} started")
            time.sleep(30)


        running_instances = get_running_instances()
        running_instance_count = len(running_instances)
        print("Running instances count is : " + str(running_instance_count))

        if running_instance_count < MAX_INSTANCES and queue_length >= SCALE_OUT_THRESHOLD:
            print("Increasing instance count")
            instance_count = str(running_instance_count+1)
            instance_name = f"app-tier-instance-{instance_count}"
            instance_id = start_instance(instance_name)
            print(f"instance with id {instance_id} started")

        
        if running_instance_count > MIN_INSTANCES and queue_length <= SCALE_IN_THRESHOLD:
            if queue_length >= 1 and running_instance_count == 1:
                print("maintaining atleast 1 running instance")
            else: 
                print('Descreasing instance count')
                stop_instance_id = get_instance_id_for_scale_in(running_instances)
                stop_instance(stop_instance_id)
                print(f"instance with id {stop_instance_id} stopped")


        print("*********************************************************************************")        
        time.sleep(30)


if __name__ == '__main__':
    main()
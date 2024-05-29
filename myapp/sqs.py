import boto3, time

request_sqs_url = 'https://sqs.us-east-1.amazonaws.com/637423519415/1227975517-req-queue'
response_sqs_url = 'https://sqs.us-east-1.amazonaws.com/637423519415/1227975517-resp-queue'


class SQS:
    
    def __init__(self):
        self.sqs = boto3.client('sqs')

    def send_request(self, request_id, bucket_name, key):

        message_attributes = {}
        message_attributes['request_id'] = {
            'DataType' : 'String',
            'StringValue' : request_id,
        }
        message_attributes['bucket_name'] = {
            'DataType' : 'String',
            'StringValue' : bucket_name
        }
        message_attributes['key'] = {
            'DataType' : 'String',
            'StringValue' : key
        }
        message_body=request_id
        
        response = self.sqs.send_message(QueueUrl=request_sqs_url, DelaySeconds=0, MessageAttributes=message_attributes, 
        MessageBody=message_body)

        return response


    def receive_request(self, message_request_id):

        while True:
            response = self.sqs.receive_message(QueueUrl=response_sqs_url, MessageAttributeNames=['All'], 
            VisibilityTimeout=0, WaitTimeSeconds=15)

            messages = response.get('Messages', [])

            for msg in messages:
                request_id = msg['MessageAttributes']['request_id']['StringValue']
                response = msg['MessageAttributes']['response']['StringValue']
                if (request_id == message_request_id):
                    return response


    def clear_sqs_queue(self, queue_name):

        while True:
        
            response = self.sqs.receive_message(QueueUrl=queue_name, MessageAttributeNames=['All'], 
            VisibilityTimeout=0, WaitTimeSeconds=15, MaxNumberOfMessages=10)
            print(response)

            messages = response.get('Messages', [])

            if messages:
                for msg in messages:
                    self.sqs.delete_message(QueueUrl=queue_name, ReceiptHandle=msg['ReceiptHandle'])
            else:
                break



            



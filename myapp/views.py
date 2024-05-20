import csv, uuid
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from myapp.s3 import S3
from myapp.sqs import SQS
from myapp.classification_mapper import mapper_results
from rest_framework.decorators import api_view


@api_view(['POST'])
def RecognizeFace(request):
    input_file = request.FILES.get('inputFile')
    input_file_formated = str(input_file)[:-4]

    request_id = str(uuid.uuid4())

    s3 = S3()
    sqs = SQS()

    #upload input image to s3
    s3.upload_object(str(input_file), input_file, settings.INPUT_S3_BUCKET)
    print("WEB TIER: uploaded input image to i/p S3 bucket")

    #upload request to Req SQS queue
    sqs.send_request(request_id, settings.INPUT_S3_BUCKET, str(input_file))
    print("WEB TIER: Sent Request to request SQS queue")

    #receive request from response SQS queue
    face_response_msg =sqs.receive_request(request_id)
    print("WEB TIER: Receive Response from response SQS queue")

    #upload output res to ouput s3 bucket
    s3.upload_object(input_file_formated, face_response_msg, settings.OUTPUT_S3_BUCKET)
    
    return HttpResponse(face_response_msg)


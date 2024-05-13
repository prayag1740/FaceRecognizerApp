import csv
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from myapp.classification_mapper import mapper_results
from rest_framework.decorators import api_view


@api_view(['POST'])
def RecognizeFace(request):
    input_file = request.FILES.get('inputFile')
    input_file_formated = str(input_file)[:-4]

    target = mapper_results[input_file_formated]
    response_text = input_file_formated + ":" + target
    
    return HttpResponse(response_text)


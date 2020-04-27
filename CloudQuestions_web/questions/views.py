from django.shortcuts import render
from django.http import HttpResponse
from .models import Topic


def index(request):
    latest_question_list = Topic.objects.order_by('-created')[:5]
    response = ', '.join([q.question for q in latest_question_list])
    return HttpResponse(response)


def detail(request, question_id):
    return HttpResponse(f'This is question {question_id}')

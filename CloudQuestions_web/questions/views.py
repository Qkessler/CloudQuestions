from django.shortcuts import render
from django.http import HttpResponse
from .models import Topic


def index(request):
    latest_question_list = Topic.objects.order_by('-created')[:5]
    context = {'question_list': latest_question_list}
    return render(request, 'questions/index.html', context)


def detail(request, question_id):
    return HttpResponse(f'This is question {question_id}')

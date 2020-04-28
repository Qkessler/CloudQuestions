from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Topic


def index(request):
    latest_question_list = Topic.objects.order_by('-created')[:5]
    context = {'question_list': latest_question_list}
    return render(request, 'questions/index.html', context)


def detail(request, topic):
    topics = Topic.objects.all()
    questions_by_topic = [t.question for t in topics if t.topic == topic]
    return render(request, 'questions/detail.html',
                  {'topic': topic,
                   'questions_by_topic': questions_by_topic})

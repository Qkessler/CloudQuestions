from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Topic
from session_factory import create_session
from models.topic import Topic


def index(request):
    session = create_session()
    # latest_question_list = Topic.objects.order_by('-created')[:5]
    # context = {'question_list': latest_question_list}
    # return render(request, 'questions/index.html', context)
    return HttpResponse('Esto es una prueba')


def detail(request, topic):
    session = create_session()
    query = session.query(Topic).filter(Topic.topic == topic)
    questions_by_topic = {topic.question:
                          topic.answer for topic in list(query)}
    session.close()
    return render(request, 'questions/detail.html',
                  {'topic': topic,
                   'questions_by_topic': questions_by_topic})

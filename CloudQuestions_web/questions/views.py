from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
# from db_folder.session_factory import create_session
from db_folder.session_factory import create_session
from models.topic import Topic
from questions.src import question_service


def index(request):
    session = create_session()
    # latest_question_list = Topic.objects.order_by('-created')[:5]
    # context = {'question_list': latest_question_list}
    # return render(request, 'questions/index.html', context)
    return HttpResponse('Esto es una prueba')


def detail(request, topic):
    questions_by_topic = question_service.questions_by_topic(topic)
    return render(request, 'questions/detail.html',
                  {'topic': topic,
                   'questions_by_topic': questions_by_topic})

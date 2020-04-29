from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .forms import SearchForm, UploadFileForm
from questions.src import question_service, parsing
import pdb


def index(request):
    context = {}
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            topic = form.cleaned_data.get('search_text')
            topics = question_service.search_engine(topic)
            db_topics = []
            for t in topics:
                db_topics.append(parsing.scrub_name(t))
            topics_return = dict(zip(topics, db_topics))
            context['topics_return'] = topics_return
    else:
        form = SearchForm()
    context['form'] = form
    return render(request, 'questions/index.html', context)


def detail(request, topic):
    questions_by_topic = question_service.questions_by_topic(topic)
    return render(request, 'questions/detail.html',
                  {'topic': topic,
                   'questions_by_topic': questions_by_topic})


def upload_file(request):
    # context = {}
    # if request.method == 'POST':
    #     # form = UploadFileForm(request.POST, request.FILES)
    #     # if form.is_valid():
    #     #     context['return_form'] = 'FORM IS VALID'
    #     #     context['file'] = request.FILES['file']
    #     # else:
    #     #     context['return_form'] = 'FROM IS INVALID'
    #     uploaded_file = request.FILES.get('file')
    #     print(uploaded_file)
    # else:
    #     form = UploadFileForm()
    # context['form'] = form
    return render(request, 'questions/file.html')

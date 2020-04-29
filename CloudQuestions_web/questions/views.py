from django.shortcuts import render
from django.http import HttpResponse
from .forms import SearchForm, UploadFileForm
from questions.src import question_service, parsing


def index(request):
    context = {}
    correct_upload = ''
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        upload_file_form = UploadFileForm(request.POST)
        if search_form.is_valid():
            topic = search_form.cleaned_data.get('search_text')
            topics = question_service.search_engine(topic)
            db_topics = []
            for t in topics:
                db_topics.append(parsing.scrub_name(t))
            topics_return = dict(zip(topics, db_topics))
            context['topics_return'] = topics_return
        elif upload_file_form.is_valid():
            uploaded = request.FILES.get('file')
            correct_upload = 'File uploaded correctly'
    else:
        search_form = SearchForm()
        upload_file_form = UploadFileForm()
    context['search_form'] = search_form
    context['upload_file_form'] = upload_file_form
    context['correct_upload'] = correct_upload
    return render(request, 'questions/index.html', context)


def detail(request, topic):
    questions_by_topic = question_service.questions_by_topic(topic)
    return render(request, 'questions/detail.html',
                  {'topic': topic,
                   'questions_by_topic': questions_by_topic})

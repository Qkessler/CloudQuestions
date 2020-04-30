from django.shortcuts import render
from django.http import HttpResponse
from .forms import SearchForm, UploadFileForm
from questions.src import question_service, parsing


def index(request):
    context = {}
    if request.method == 'POST':
        search_form = SearchForm(prefix='search_form')
        upload_file_form = UploadFileForm(prefix='upload_file_form')
        # We check whether is the search or upload_file_form.
        action = request.POST.get('action')

        if action == 'search':
            search_form = SearchForm(request.POST, prefix='search_form')
            if search_form.is_valid():
                topic = search_form.cleaned_data.get('search_text')
                topics = question_service.search_engine(topic)
                db_topics = []
                for t in topics:
                    db_topics.append(parsing.scrub_name(t))
                    topics_return = dict(zip(topics, db_topics))
                    context['topics_return'] = topics_return
        elif action == 'upload':
            upload_file_form = UploadFileForm(request.POST, request.FILES)
            if upload_file_form.is_valid():
                uploaded = request.FILES.get('file')
                print(uploaded)
    else:
        search_form = SearchForm(prefix='search_form')
        upload_file_form = UploadFileForm(prefix='upload_file_form')
    context['search_form'] = search_form
    context['upload_file_form'] = upload_file_form
    return render(request, 'questions/index.html', context)


def detail(request, topic):
    questions_by_topic = question_service.questions_by_topic(topic)
    return render(request, 'questions/detail.html',
                  {'topic': topic,
                   'questions_by_topic': questions_by_topic})

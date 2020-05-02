from django.shortcuts import render
from django.http import HttpResponse
from .forms import SearchForm, UploadFileForm
from questions.src import question_service, parsing
import pdb


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
                search_term = search_form.cleaned_data.get('search_text')
                db_topics = question_service.search_engine(search_term)
                topics = []
                for t in db_topics:
                    topics.append(parsing.unscrub_name(t))
                    topics_return = dict(zip(db_topics, topics))
                    context['topics_return'] = topics_return
        elif action == 'upload':
            upload_file_form = UploadFileForm(request.POST, request.FILES)
            if upload_file_form.is_valid():
                uploaded = request.FILES.get('file')
                parsing.handling_uploaded_file(uploaded)
                print('I went through handling the file.')
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


def random_questions(request, topic):
    context = {}
    random_question = question_service.random_question(topic)
    context['random_question'] = random_question
    context['topic'] = topic
    return render(request, 'questions/random.html', context)

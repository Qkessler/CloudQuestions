from django.shortcuts import render, redirect
from .forms import SearchForm, UploadFileForm
from questions.src import question_service, parsing
from .models import Topic

QUESTION_LIST = []


def index(request):
    context = {}
    topics_return = []
    context['searched'] = False
    context['empty'] = True
    if request.method == 'POST':
        search_form = SearchForm(prefix='search_form')
        upload_file_form = UploadFileForm(prefix='upload_file_form')
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
                    context['empty'] = False
                context['searched'] = True
        elif action == 'upload':
            upload_file_form = UploadFileForm(request.POST, request.FILES)
            if upload_file_form.is_valid():
                uploaded = request.FILES.get('file')
                parsing.handling_uploaded_file(uploaded)
    else:
        search_form = SearchForm(prefix='search_form')
        upload_file_form = UploadFileForm(prefix='upload_file_form')
    context['search_form'] = search_form
    context['upload_file_form'] = upload_file_form
    context['all_topics'] = {topic.name: parsing.unscrub_name(topic.name)
                             for topic in Topic.objects.all()}
    context['topics_return'] = topics_return
    return render(request, 'questions/index.html', context)


def detail(request, topic):
    global QUESTION_LIST
    questions_by_topic = question_service.questions_by_topic(topic)
    color = None
    if request.GET.get('red_button') == 'Bad':
        color = 'red'
    elif request.GET.get('yellow_button') == 'Medium':
        color = 'yellow'
    elif request.GET.get('green_button') == 'Good':
        color = 'green'
    if color:
        question_service.update_stats(topic, color, request.user)
        return redirect('accounts:settings', topic, color)
    if request.GET.get('random'):
        QUESTION_LIST.clear()
        return redirect('questions:random', topic)
    return render(request, 'questions/detail.html',
                  {'topic': topic,
                   'questions_by_topic': questions_by_topic})


def random_questions(request, topic):
    global QUESTION_LIST
    context = {}
    breakpoint()
    if request.GET.get('next_question') or len(QUESTION_LIST) == 0:
        random_question = question_service.random_question(
            topic, QUESTION_LIST)
        if random_question:
            QUESTION_LIST.append(random_question)
            if not random_question:
                return redirect('questions:detail', topic)
        return redirect('questions:random', topic)
    if request.GET.get('return'):
        return redirect('questions:detail', topic)
    context['random_question'] = random_question
    context['topic'] = topic
    return render(request, 'questions/random.html', context)


def login(request):
    return render(request, 'questions/login.html')

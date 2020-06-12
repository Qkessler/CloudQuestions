from django.shortcuts import render, redirect
from .forms import (SearchForm, UploadFileForm,
                    CreateTopicForm, CreateQuestionForm)
from questions.src import question_service, parsing
from .models import Topic, Question
from accounts.src import api_client


def index(request):
    return render(request, 'questions/index.html')


def questions(request, toggle_help=None):
    context = {}
    topics_searched = []
    context['searched'] = False
    context['empty'] = True
    context['help'] = 'help_false'
    if toggle_help:
        context['help'] = 'help_true'
    if request.GET.get('toggle_help'):
        if toggle_help == "true":
            return redirect('questions:questions')
        return redirect('questions:questions', 'true')
    if request.GET.get('upload_topic'):
        return redirect('questions:create_topic')
    if request.method == 'POST':
        search_form = SearchForm(prefix='search_form')
        upload_file_form = UploadFileForm(prefix='upload_file_form')
        action = request.POST.get('action')

        if action == 'search':
            search_form = SearchForm(request.POST, prefix='search_form')
            if search_form.is_valid():
                search_term = search_form.cleaned_data.get('search_text')
                db_topics = question_service.search_engine(
                    search_term, request.user)
                unscrubed_topics = []
                for topic in db_topics:
                    unscrubed_topics.append(parsing.unscrub_name(topic.name))
                topics_searched = dict(zip(db_topics, unscrubed_topics))
                context['empty'] = False
                context['searched'] = True
        elif action == 'upload':
            upload_file_form = UploadFileForm(request.POST, request.FILES)
            if upload_file_form.is_valid():
                uploaded = request.FILES.get('file')
                parsing.handling_uploaded_file(uploaded, request.user)
    else:
        search_form = SearchForm(prefix='search_form')
        upload_file_form = UploadFileForm(prefix='upload_file_form')
    context['search_form'] = search_form
    context['upload_file_form'] = upload_file_form
    all_topics = {topic: parsing.unscrub_name(topic.name)
                  for topic in Topic.objects.all().
                  filter(creator=request.user).order_by('name')}
    if len(all_topics) > 50:
        all_topics = all_topics[:50]
    if len(topics_searched) > 50:
        topics_searched = topics_searched[:50]
    context['topics_searched'] = topics_searched
    context['all_topics'] = all_topics
    return render(request, 'questions/questions.html', context)


def detail(request, topic):
    questions_by_topic = question_service.questions_by_topic(topic)
    color = None
    context = {}
    context['is_creator'] = False
    creator = question_service.get_creator(topic)
    context['creator'] = creator.username
    if creator.id == request.user.id:
        context['is_creator'] = True
    if request.GET.get('delete') and context['creator']:
        topic_id = question_service.topics_by_id(topic)[0]
        topic = Topic.objects.get(id=topic_id)
        topic.delete()
        return redirect('questions:questions')
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
        return redirect('questions:random', topic, ' ')
    context['topic_pretty_name'] = parsing.unscrub_name(topic)
    topic_id = question_service.topics_by_id(topic)[0]
    topic = Topic.objects.get(id=topic_id)
    context['topic'] = topic
    context['questions_by_topic'] = questions_by_topic
    return render(request, 'questions/detail.html', context)


def browse(request):
    context = {}
    topics_searched = []
    context['searched'] = False
    context['empty'] = True
    if request.method == 'POST':
        search_form = SearchForm(prefix='search_form')
        action = request.POST.get('action')

        if action == 'search':
            search_form = SearchForm(request.POST, prefix='search_form')
            if search_form.is_valid():
                search_term = search_form.cleaned_data.get('search_text')
                db_topics = question_service.search_engine(search_term)
                unscrubed_topics = []
                for topic in db_topics:
                    unscrubed_topics.append(parsing.unscrub_name(topic.name))
                topics_searched = dict(zip(db_topics, unscrubed_topics))
                context['empty'] = False
                context['searched'] = True
    else:
        search_form = SearchForm(prefix='search_form')
    context['search_form'] = search_form
    all_topics = {topic: parsing.unscrub_name(topic.name)
                  for topic in Topic.objects.all()}
    if len(all_topics) > 50:
        all_topics = all_topics[:50]
    if len(topics_searched) > 50:
        topics_searched = topics_searched[:50]
    context['topics_searched'] = topics_searched
    context['all_topics'] = all_topics
    return render(request, 'questions/browse.html', context)


def random_questions(request, topic, list_questions=''):
    context = {}
    questions_list = question_service.get_list_questions(list_questions)
    first_question = len(questions_list) == 0
    if request.GET.get('next_question') or first_question:
        random_question = question_service.random_question(
            topic, questions_list)
        if random_question:
            questions_list.append(random_question)
            str_list = question_service.create_question_list(questions_list)
            return redirect('questions:random', topic, str_list)
        return redirect('questions:detail', topic)
    if request.GET.get('return'):
        return redirect('questions:detail', topic)
    context['topic_pretty_name'] = parsing.unscrub_name(topic)
    topic_id = question_service.topics_by_id(topic)[0]
    topic_context = Topic.objects.get(id=topic_id)
    context['topic'] = topic_context
    context['creator'] = topic_context.creator
    context['random_question'] = question_service.question_by_position(
        topic, questions_list[-1])
    return render(request, 'questions/random.html', context)


def login(request):
    return render(request, 'questions/login.html')


def create_topic(request, topic_added=None):
    context = {}
    if topic_added:
        list_args = topic_added.split('+')
        topic = list_args[0]
        added = list_args[1]
        if len(list_args) > 2:
            created = list_args[2]
            topic_id = question_service.topics_by_id(topic)[0]
            list_questions = {question.question: question.answer
                              for question in Question.objects.
                              all().filter(topic=topic_id)}
            context['list_questions'] = list_questions
            context['created'] = created
        context['topic'] = topic
        context['added'] = added
    if request.method == 'POST':
        create_topic_form = CreateTopicForm(prefix='create_topic_form')
        create_question_form = CreateQuestionForm(prefix='upload_file_form')
        action = request.POST.get('action')
        if action == 'create_topic':
            create_topic_form = CreateTopicForm(
                request.POST, prefix='create_topic_form')
            if create_topic_form.is_valid():
                topic_name = create_topic_form.cleaned_data.get('name')
                added = True
                topic_added = topic_name + '+' + str(added)
                return redirect('questions:create_topic', topic_added)
        elif action == 'create_question':
            create_question_form = CreateQuestionForm(
                request.POST, prefix='create_question_form')
            if create_question_form.is_valid():
                topic_name = request.POST.get('topic_name')
                topic_created = Topic.objects.all().filter(name=topic_name)
                question = create_question_form.cleaned_data.get(
                    'question')
                answer = create_question_form.cleaned_data.get('answer')
                if not topic_created:
                    topic_created = Topic()
                    topic_created.name = topic_name
                    topic_created.color = api_client.random_color()
                    topic_created.creator = request.user
                    topic_created.save()
                else:
                    topic_created = topic_created[0]
                created_question = Question()
                created_question.topic = topic_created
                created_question.question = question
                created_question.answer = answer
                created_question.save()
                topic_added = topic_name + '+' + \
                    'True' + '+' + 'created'
                return redirect('questions:create_topic',
                                topic_added)
    else:
        create_topic_form = CreateTopicForm(prefix='create_topic_form')
        create_question_form = CreateQuestionForm(
            prefix='create_question_form')
        if request.GET.get('delete'):
            topic_id = question_service.topics_by_id(topic)[0]
            topic = Topic.objects.get(id=topic_id)
            topic.delete()
            return redirect('questions:create_topic')
    context['create_topic_form'] = create_topic_form
    context['create_question_form'] = create_question_form
    return render(request, 'questions/create_topic.html', context)

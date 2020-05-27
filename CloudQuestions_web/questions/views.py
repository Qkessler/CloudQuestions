from django.shortcuts import render, redirect
from .forms import (SearchForm, UploadFileForm,
                    CreateTopicForm, CreateQuestionForm)
from questions.src import question_service, parsing
from .models import Topic, Question


def index(request):
    context = {}
    topics_return = []
    context['searched'] = False
    context['empty'] = True
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
                db_topics = question_service.search_engine(search_term)
                topics = []
                for topic in db_topics:
                    topics.append(parsing.unscrub_name(topic))
                    topics_return = dict(zip(db_topics, topics))
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
    context['all_topics'] = {topic.name: parsing.unscrub_name(topic.name)
                             for topic in Topic.objects.all()}
    context['topics_return'] = topics_return
    return render(request, 'questions/index.html', context)


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
        return redirect('questions:index')
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
    context['topic'] = topic
    context['questions_by_topic'] = questions_by_topic
    return render(request, 'questions/detail.html', context)


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
        print(list_questions)
        return redirect('questions:detail', topic)
    if request.GET.get('return'):
        return redirect('questions:detail', topic)
    context['topic'] = topic
    context['random_question'] = question_service.question_by_position(
        topic, questions_list[-1])
    return render(request, 'questions/random.html', context)


def login(request):
    return render(request, 'questions/login.html')


def create_topic(request, topic_added=None):
    context = {}
    breakpoint()
    if topic_added:
        list_args = topic_added.split('+')
        topic = list_args[0]
        added = list_args[1]
        if len(list_args) > 2:
            created = list_args[2]
            topic_id = question_service.topics_by_id(topic)[0]
            list_questions = [
                question.question for question in Question.objects
                .all().filter(id=topic_id)]
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
                topic_created = Topic.objects.get_or_create(name=topic)
                question = create_question_form.cleaned_data.get(
                    'question')
                answer = create_question_form.cleaned_data.get('answer')
                if topic:
                    created_question = Question()
                    created_question.topic = topic_created
                    created_question.question = question
                    created_question.question = answer
                    created_question.save()
                    return redirect('questions:create_topic',
                                    topic_added + '+' + 'created')
    else:
        create_topic_form = CreateTopicForm(prefix='create_topic_form')
        create_question_form = CreateQuestionForm(
            prefix='create_question_form')
    context['create_topic_form'] = create_topic_form
    context['create_question_form'] = create_question_form
    return render(request, 'questions/create_topic.html', context)

from django.shortcuts import render, redirect
from .forms import SearchForm, UploadFileForm, CreateTopicForm, CreateTopicFormId
from questions.src import question_service, parsing
from .models import Topic, Question
from django.http import HttpResponse


def index(request):
    return render(request, "questions/index.html")


def questions(request):
    context = {}
    topics_searched = []
    context["searched"] = False
    context["empty"] = True
    search_form = SearchForm(prefix="search_form")
    upload_file_form = UploadFileForm(prefix="upload_file_form")
    question_service.delete_flagged()
    if request.GET.get("toggle_help"):
        return redirect("questions:detail", "CloudQuestions_Help")
    if request.GET.get("upload_topic"):
        return redirect("questions:create_topic")
    if request.method == "POST":
        if "search" in request.POST.values():
            # We are using the values because forms in crispy-forms are weird,
            # and the hidden element only works in as is in model forms. The
            # hidden element in forms is called <name_form>-<name_hidden>.
            search_form = SearchForm(request.POST, prefix="search_form")
            if search_form.is_valid():
                search_term = search_form.cleaned_data.get("search_text")
                db_topics = question_service.search_engine(
                    search_term, creator=request.user
                )
                unscrubed_topics = []
                for topic in db_topics:
                    unscrubed_topics.append(parsing.unscrub_name(topic.name))
                topics_searched = dict(zip(db_topics, unscrubed_topics))
                context["empty"] = False
                context["searched"] = True
        elif "upload" in request.POST.values():
            upload_file_form = UploadFileForm(request.POST, request.FILES)
            if upload_file_form.is_valid():
                uploaded = request.FILES.get("file")
                return_dict = parsing.handling_uploaded_file(uploaded, request.user)
                return redirect("questions:create_topic", return_dict["topic_id"])
    context["search_form"] = search_form
    context["upload_file_form"] = upload_file_form
    all_topics = {
        topic: parsing.unscrub_name(topic.name)
        for topic in Topic.objects.all().filter(creator=request.user).order_by("name")
    }
    if len(all_topics) > 50:
        all_topics = all_topics[:50]
    if len(topics_searched) > 50:
        topics_searched = topics_searched[:50]
    context["topics_searched"] = topics_searched
    context["all_topics"] = all_topics
    return render(request, "questions/questions.html", context)


def detail(request, topic_name):
    if request.GET.get("toggle_help"):
        return redirect("questions:detail", "CloudQuestions_Help")
    color = None
    context = {}
    context["is_creator"] = False
    topic = question_service.get_topic(topic_name)
    creator = question_service.get_creator(topic_name)
    context["creator"] = creator.username
    if creator.id == request.user.id:
        context["is_creator"] = True

    is_public = topic.privacy
    group_participant = question_service.is_participant(request.user, topic)
    help_topic = topic_name == "CloudQuestions_Help"
    if is_public or context["is_creator"] or group_participant or help_topic:

        if request.GET.get("delete") and context["creator"]:
            topic.delete()
            return redirect("questions:questions")

        if request.GET.get("privacy-button.x"):
            topic.privacy = not topic.privacy
            topic.save()

        if request.GET.get("modify-button.x"):
            return redirect("questions:create_topic", topic.id)

        if request.GET.get("red_button") == "Bad":
            color = "red"
        elif request.GET.get("yellow_button") == "Medium":
            color = "yellow"
        elif request.GET.get("green_button") == "Good":
            color = "green"
        if color:
            question_service.update_stats(topic_name, color, request.user)
            return redirect("accounts:settings", topic_name, color)

        if request.GET.get("random"):
            return redirect("questions:random", topic_name, " ")

        context["topic_pretty_name"] = parsing.unscrub_name(topic_name)
        context["topic"] = topic
        questions_by_topic = question_service.questions_by_topic_name(topic_name)
        context["questions_by_topic"] = questions_by_topic
        context["public"] = question_service.get_privacy(topic_name)
        return render(request, "questions/detail.html", context)
    return redirect("questions:browse")


def browse(request, number_questions=10):
    if request.GET.get("toggle_help"):
        return redirect("questions:detail", "CloudQuestions_Help")
    context = {}
    topics_searched = []
    context["searched"] = False
    context["empty"] = True
    if number_questions % 10 != 0:
        return HttpResponse(status="404")
    if request.method == "POST":
        search_form = SearchForm(prefix="search_form")
        action = request.POST.get("action")

        if action == "search":
            search_form = SearchForm(request.POST, prefix="search_form")
            if search_form.is_valid():
                search_term = search_form.cleaned_data.get("search_text")
                db_topics = question_service.search_engine(search_term)
                unscrubed_topics = []
                for topic in db_topics:
                    unscrubed_topics.append(parsing.unscrub_name(topic.name))
                topics_searched = dict(zip(db_topics, unscrubed_topics))
                topics_searched_items = list(topics_searched.items())
                context["topics_searched"] = topics_searched_items
                context["empty"] = False
                context["searched"] = True
    else:
        search_form = SearchForm(prefix="search_form")

    context["search_form"] = search_form
    if context["searched"]:
        topics_items = topics_searched_items
    else:
        all_topics = {
            topic: parsing.unscrub_name(topic.name)
            for topic in Topic.objects.all().filter(privacy=True)
        }
        topics_items = list(all_topics.items())
    if len(topics_items) + number_questions > 20:
        context["more"] = True
    if request.GET.get("next_topics"):
        return redirect("questions:browse", number_questions + 10)
    if number_questions > 10:
        if len(topics_items) > number_questions:
            number = number_questions - 10
            context["all_topics"] = topics_items[number:number_questions]
        elif len(topics_items) > number_questions + 10:
            number = number_questions + 10
            context["all_topics"] = topics_items[number_questions:number]
        else:
            length = len(topics_items)
            context["all_topics"] = topics_items[number_questions - 10 : length]
            context["more"] = False
    else:
        context["all_topics"] = topics_items[:10]
    return render(request, "questions/browse.html", context)


def random_questions(request, topic_name, list_questions=""):
    context = {}
    questions_list = question_service.get_list_questions(list_questions)
    first_question = len(questions_list) == 0
    if request.GET.get("next_question") or first_question:
        random_question = question_service.random_question(topic_name, questions_list)
        if random_question:
            questions_list.append(random_question)
            str_list = question_service.create_question_list(questions_list)
            return redirect("questions:random", topic_name, str_list)
        return redirect("questions:detail", topic_name)
    if request.GET.get("return"):
        return redirect("questions:detail", topic_name)
    context["topic_pretty_name"] = parsing.unscrub_name(topic_name)
    context["topic"] = question_service.get_topic(topic_name)
    context["creator"] = context["topic"].creator
    context["random_question"] = question_service.question_by_position(
        topic_name, questions_list[-1]
    )
    return render(request, "questions/random.html", context)


def login(request):
    return render(request, "questions/login.html")


def create_topic(request, topic_id=None):
    context = {}
    if not topic_id:
        topic_form = CreateTopicForm(prefix="create_topic_form")
    else:
        topic_form = CreateTopicFormId(prefix="create_topic_id_form")
    if request.GET.get("toggle_help"):
        return redirect("questions:detail", "CloudQuestions_Help")
    if request.method == "POST":
        if not topic_id:
            topic_form = CreateTopicForm(request.POST, prefix="create_topic_form")
            if topic_form.is_valid():
                topic_name = parsing.scrub_name(topic_form.cleaned_data["name"])
                question = topic_form.cleaned_data["question"]
                answer = topic_form.cleaned_data["answer"]
                user = request.user
                topic_com = question_service.create_or_modify(
                    topic_name, question, answer, user
                )
                return redirect("questions:create_topic", topic_com.id)
        else:
            topic_form = CreateTopicFormId(request.POST, prefix="create_topic_id_form")
            if topic_form.is_valid():
                topic_name = Topic.objects.get(id=topic_id).name
                question = topic_form.cleaned_data["question"]
                answer = topic_form.cleaned_data["answer"]
                user = request.user
                topic_com = question_service.create_or_modify(
                    topic_name, question, answer, user
                )
                return redirect("questions:create_topic", topic_com.id)
    else:
        if topic_id:
            topic_url = Topic.objects.get(id=topic_id)
            if topic_url and topic_url.creator == request.user:
                context["topic_pretty_name"] = parsing.unscrub_name(topic_url.name)
                context["topic"] = topic_url
                context["enough_size"] = (
                    Question.objects.filter(topic=topic_url).count() > 1
                )
                list_by_topic = question_service.questions_by_topic_name(topic_url.name)
                context["list_by_topic"] = list_by_topic
                if request.GET.get("remove-button.x"):
                    question_id = request.GET.get("action")
                    question_to_remove = question_service.get_question(question_id)
                    question_to_remove.delete()
                if request.GET.get("add_topic"):
                    topic_url.created_flag = True
                    for question in context["list_by_topic"]:
                        if not question.added_flag:
                            question.added_flag = True
                            question.save()
                    topic_url.save()
                    return redirect("questions:questions")

    context["topic_form"] = topic_form
    return render(request, "questions/create_topic.html", context)

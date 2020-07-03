import random
import questions.src.parsing as parsing
from questions.models import Topic, Question, Rating, CalendarConnection
from accounts.src.api_client import random_color
import markdown


def include_questions(q_a, topic_name, user):    # pragma: no cover
    """ Inserting the questions and answers in the db. """
    topics = list(Topic.objects.all())
    if topic_name not in [topic.name for topic in topics]:
        topic = Topic()
        topic.name = topic_name
        topic.color = random_color()
        topic.creator = user
        topic.save()
    else:
        topic = Topic.objects.get(name=topic_name)
    for question_el, answer_el in q_a.items():
        if not same_questions(question_el, topic_name) and not same_answers(
                answer_el, topic_name):
            question = Question()
            question.topic = topic
            question.question = question_el
            question.answer = answer_el
            question.save()


def questions_by_topic(topic_name):
    """ Query of questions given a topic name. """
    topic_ids = topics_by_id(topic_name)
    questions = Question.objects.filter(topic__in=topic_ids)
    return questions


def same_questions(question, topic):
    """ Returns a boolean indicating whether the same question already exists
    in the db for a given topic. """
    topic = Topic.objects.get(name=topic)
    if topic:
        topic_id = topic.id
        query_questions = Question.objects.filter(topic=topic_id).filter(
            question=question)
        if not query_questions:
            return False
        return True
    return False


def same_answers(answer, topic):
    topic = Topic.objects.get(name=topic)
    if topic:
        topic_id = topic.id
        query_answers = Question.objects.filter(
            answer=answer).filter(topic=topic_id)
        if not query_answers:
            return False
        return True
    return False


def topics_by_name(ids, creator=None):
    """ Function that given a list of ids searches for the corresponding
    names in the db. """
    topic_names = []
    if not creator:
        query = Topic.objects.filter(id__in=ids)
        topic_names = [topic.name for topic in query]
    else:
        query_creator = Topic.objects.filter(
            id__in=ids).filter(creator=creator)
        topic_names = [topic.name for topic in query_creator]
    return topic_names


def topics_by_id(name, creator=None):
    """ Function that given a name searches for the corresponding
ids in the db. """
    topic_ids = []
    if not creator:
        query = Topic.objects.filter(name__contains=name)
        topic_ids = [topic.id for topic in query]
    else:
        query_creator = Topic.objects.filter(
            name__contains=name).filter(creator=creator)
        topic_ids = [topic.id for topic in query_creator]
    return topic_ids


def get_words(question):
    """ Gets the words of a question. """
    text = question.question
    return [parsing.scrub_name(word) for word in text.split(' ')]


def search_engine(search_term, creator=None):
    """ Checks if the search_term is any of the topics first. Returns the topics
    where we have any question that contains the search_term given by the user.
    The creator is the decider to which search_engine to use, depending if
    the user is in the questions or the browse view. """
    if not creator:
        topics_ids = []
        topic_id_query = topics_by_id(parsing.scrub_name(search_term))
        if topic_id_query:
            topics_ids = topic_id_query
        query = Question.objects.all()
        topic_question = {}
        for question in query:
            if question.topic not in topic_question.keys():
                topic_question[question.topic] = []
            topic_question[question.topic].append(question)

        for topic, questions in topic_question.items():
            words_topic = []
            for question in questions:
                for word in get_words(question):
                    if word != '':
                        words_topic.append(word)
            if search_term in words_topic:
                if topic not in topics_ids:
                    topics_ids.append(topic.id)
        topics_return = Topic.objects.all().filter(
            id__in=topics_ids).order_by('name')
    else:
        topics_ids = []
        topic_id_query = topics_by_id(parsing.scrub_name(search_term), creator)
        if topic_id_query:
            topics_ids = topic_id_query
        query = Question.objects.all().filter(topic__in=topics_ids)
        topic_question = {}
        for question in query:
            if question.topic not in topic_question.keys():
                topic_question[question.topic] = []
            topic_question[question.topic].append(question)

        for topic, questions in topic_question.items():
            words_topic = []
            for question in questions:
                for word in get_words(question):
                    if word != '':
                        words_topic.append(word)
            if search_term in words_topic:
                if topic not in topics_ids:
                    topics_ids.append(topic.id)
        topics_return = Topic.objects.all().filter(
            id__in=topics_ids).order_by('name')
    return topics_return


def random_question(topic, questions_showed):
    """ Function that returns a random question for a topic. """
    topic_id = Topic.objects.filter(name=topic)[0].id
    len_query = Question.objects.filter(topic=topic_id).count()
    question_id = None
    if len(questions_showed) == len_query:
        return None
    while question_id is None or question_id in questions_showed:
        question_id = random.randrange(
            0, len_query) + 1
    return question_id


def update_stats(topic_name, color, user):
    """ Given the color of the rating for the topic studied, creates
    a rating instance in the db. """
    topic = Topic.objects.get(name=topic_name)
    rating = Rating()
    rating.rating = color
    rating.topic = topic
    rating.user = user
    rating.save()


def create_table(user):
    """ Creates the dict to set the data in the view. """
    ratings_user = Rating.objects.all().filter(user=user)
    table = {}
    for rating in ratings_user:
        topic_id = rating.topic
        if topic_id not in table.keys():
            table[topic_id] = []
        table[topic_id].append(rating)
    return table


def get_calendar(user):
    """ Gets calendar preference for the user. """
    user_calendar = CalendarConnection.objects.get(user=user)
    return user_calendar.connection


def create_calendar_connection(user):
    """ Creates the instance of the calendar_connection db entry,
    when a new user is registered. """
    calendar_boolean = CalendarConnection()
    calendar_boolean.user = user
    calendar_boolean.save()


def change_calendar_connection(user):
    """ Function that changes the calendar_connection entry
    for the user, inverting the value before."""
    user_calendar = CalendarConnection.objects.get(user=user)
    if user_calendar.connection:
        user_calendar.connection = False
    else:
        user_calendar.connection = True
    user_calendar.save()


def get_color(topic):
    """ Function that given a topic, gets the color from db. """
    topic_id = topics_by_id(topic)[0]
    color = Topic.objects.get(id=topic_id).color
    return color


def get_creator(topic):
    """ Functions that returns the creator of a given topic. """
    topic_id = topics_by_id(topic)[0]
    creator = Topic.objects.get(id=topic_id).creator
    return creator


def get_list_questions(list_questions):
    """ Function that given a string, gets the list of questions
    for the random view. """
    if not list_questions.strip():
        return []
    questions_list = [int(string) for string in list_questions.split('+')]
    return questions_list


def create_question_list(question_list):
    """ Function that creates a string for the questions_list given. """
    string = '+'.join([str(id) for id in question_list])
    return string


def question_by_position(topic, position):
    """ Return a question given the id. """
    topic_id = topics_by_id(topic)[0]
    questions = Question.objects.all().filter(topic=topic_id)
    return questions[position - 1]


def create_or_modify(topic_name, question, answer, user):
    """ Creates or modifies a topic based if we have topics with the name
    entered and the user is the creator. """
    query_ids = topics_by_id(topic_name)
    topic_com = None
    for topic_id in query_ids:
        topic = Topic.objects.get(id=topic_id)
        if topic.creator == user:
            topic_com = topic
            break
    if not topic_com:
        topic_to_add = Topic()
        topic_to_add.name = parsing.scrub_name(topic_name)
        topic_to_add.color = random_color()
        topic_to_add.creator = user
        topic_to_add.created_flag = False
        topic_to_add.save()
        topic_com = topic_to_add
    # In case the user wants to add questions to an existing topic.
    question_to_add = Question()
    question_to_add.topic = topic_com
    question_to_add.question = markdown.markdown(question)
    question_to_add.answer = markdown.markdown(answer)
    question_to_add.added_flag = False
    question_to_add.save()
    return topic_com


def delete_flagged():
    """ This is a function created to make sure that the topics with less
    than 2 questions created by the user, or the case that the user leaves
    create_topic view, are deleted. """
    query_flagged = Topic.objects.filter(created_flag=False)
    for topic in query_flagged:
        topic.delete()
    query_flagged = Question.objects.filter(added_flag=False)
    for question in query_flagged:
        question.delete()


def get_privacy(topic):
    """ Function created to get the context for the detail form, which puts and 
    icon if the topic is public"""
    topic_id = topics_by_id(topic)[0]
    topic = Topic.objects.get(id=topic_id)
    return topic.privacy


def get_question(question_id):
    """ Given an id, gets question from db."""
    return Question.objects.get(id=question_id)

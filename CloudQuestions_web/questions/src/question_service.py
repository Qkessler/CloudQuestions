import random
import questions.src.parsing as parsing
from questions.models import Topic, Question, Rating, CalendarConnection
from accounts.src.api_client import random_color


def include_questions(q_a, topic_name):    # pragma: no cover
    """ Inserting the questions and answers in the db. """
    topics = list(Topic.objects.all())
    if topic_name not in [topic.name for topic in topics]:
        topic = Topic()
        topic.name = topic_name
        topic.color = random_color()
        topic.save()
    else:
        topic = Topic.objects.get(name=topic_name)
    for question_el, answer_el in q_a.items():
        if not same_questions(question_el, topic_name):
            question = Question()
            question.topic = topic
            question.question = question_el
            question.answer = answer_el
            question.save()


def questions_by_topic(topic):
    """ Query of questions given a topic. """
    topic_ids = topics_by_id(topic)
    questions = Question.objects.filter(topic__in=topic_ids)
    questions = {question.question: question.answer
                 for question in questions}
    return questions


def same_questions(question, topic):
    """ Returns a boolean indicating whether the same question already exists
    in the db for a given topic. """
    topic = Topic.objects.get(name=topic)
    if topic:
        topic_id = topic.id
        query = Question.objects.filter(
            question=question).filter(topic=topic_id)
        if not query:
            return False
        return True
    return False


def topics_by_name(ids):
    """ Function that given a list of ids searches for the corresponding
    names in the db. """
    query = Topic.objects.filter(id__in=ids)
    topic_names = [topic.name for topic in query]
    return topic_names


def topics_by_id(name):
    """ Function that given a name searches for the corresponding
ids in the db. """
    query = Topic.objects.filter(name__contains=name)
    topic_ids = [topic.id for topic in query]
    return topic_ids


def get_words(question):
    """ Gets the words of a question. """
    text = question.question
    return [parsing.scrub_name(word) for word in text.split(' ')]


def search_engine(string):
    """ Checks if string isany of the topics first. Returns the topics
    where we have any question that contains the string given by the user. """
    topics_ids = []
    topic_id_query = topics_by_id(parsing.scrub_name(string))
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
        if string in words_topic:
            if topic not in topics_ids:
                topics_ids.append(topic.id)
    topics_return = topics_by_name(topics_ids)
    return topics_return


def random_question(topic, questions_showed):
    """ Function that returns a random question for a topic. """
    topic_id = Topic.objects.filter(name=topic)[0].id
    query = Question.objects.filter(topic=topic_id)
    len_query = len(query)
    question = None
    if len(questions_showed) == len_query:
        return None
    while question is None or question in questions_showed:
        random_number = random.randrange(
            0, query.count())
        question = query[random_number]
    return question


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

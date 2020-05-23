import random
import questions.src.parsing as parsing
from questions.models import Topic, Question, Rating, CalendarConnection
from accounts.src.api_client import get_url, get_flow, calendar_connection


# Inserting the questions and answers in the db.
def include_questions(q_a, topic_name):    # pragma: no cover
    topics = list(Topic.objects.all())
    if topic_name not in topics:
        topic = Topic()
        topic.name = topic_name
        topic.save()
    else:
        topic = Topic.objects.get(name=topic_name)
    for q, a in q_a.items():
        if not same_questions(q, topic_name):
            question = Question()
            question.topic = topic
            question.question = q
            question.answer = a
            question.save()


# Query of questions given a topic
def questions_by_topic(topic):
    topic_ids = topics_by_id(topic)
    questions = Question.objects.filter(topic__in=topic_ids)
    questions = {question.question: question.answer
                 for question in questions}
    return questions


# Returns a boolean indicating whether the same question already exists
# in the db for a given topic.
def same_questions(question, topic):
    topic = Topic.objects.get(name=topic)
    if topic:
        topic_id = topic.id
        query = Question.objects.filter(
            question=question).filter(topic=topic_id)
        if not query:
            return False
        else:
            return True
    else:
        return False


# Function that given a list of ids searches for the corresponding
# names in the db.
def topics_by_name(ids):
    query = Topic.objects.filter(id__in=ids)
    topic_names = [topic.name for topic in query]
    return topic_names


# Function that given a name searches for the corresponding
# ids in the db.
def topics_by_id(name):
    query = Topic.objects.filter(name__contains=name)
    topic_ids = [topic.id for topic in query]
    return topic_ids


# Gets the words of a question
def get_words(question):
    text = question.question
    return [parsing.scrub_name(word) for word in text.split(' ')]


# Checks if string isany of the topics first. Returns the topics
# where we have any question that contains the string given by the user.
def search_engine(string):
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


# Function that returns a random question for a topic.
def random_question(topic, questions_showed):
    topic_id = Topic.objects.filter(name=topic)[0].id
    query = Question.objects.filter(topic=topic_id)
    len_query = len([question for question in query])
    question = None
    if len(questions_showed) == len_query:
        return None
    while question == None or question in questions_showed:
        random_number = random.randrange(
            0, query.count())
        question = query[random_number]
    return question


# Given the color of the rating for the topic studied, creates
# a rating instance in the db.
def update_stats(topic_name, color, user):
    topic = Topic.objects.get(name=topic_name)
    rating = Rating()
    rating.rating = color
    rating.topic = topic
    rating.user = user
    rating.save()


# Creates the dict to set the data in the view.
def create_table(user):
    ratings_user = Rating.objects.all().filter(user=user)
    table = {}
    for rating in ratings_user:
        topic_id = rating.topic
        if topic_id not in table.keys():
            table[topic_id] = []
        table[topic_id].append(rating)
    return table


# Gets calendar preference for the user.
def get_calendar(user):
    user_calendar = CalendarConnection.objects.get(user=user)
    return user_calendar.connection


# Creates the instance of the calendar_connection db entry,
# when a new user is registered.
def create_calendar_connection(user):
    calendar_boolean = CalendarConnection()
    calendar_boolean.user = user
    calendar_boolean.save()


# Function that changes the calendar_connection entry
# for the user, inverting the value before.
def change_calendar_connection(user):
    user_calendar = CalendarConnection.objects.get(user=user)
    if user_calendar.connection:
        user_calendar.connection = False
    else:
        user_calendar.connection = True
    user_calendar.save()

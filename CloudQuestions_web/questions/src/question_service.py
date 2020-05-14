from questions.models import Topic, Question, Rating
import questions.src.parsing as parsing
from pprint import pprint as pp
import random


# Inserting the questions and answers in the db.
def include_questions(q_a, topic_name):    # pragma: no cover
    breakpoint()
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
        query = Question.objects.filter(question=question).filter(topic=topic_id)
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


# Checks if string is any of the topics first. Returns the topics
# where we have any question that contains the string given by the user.
def search_engine(string):
    topics_ids = []
    topic_id_query = topics_by_id(parsing.scrub_name(string))
    if topic_id_query:
        topics_ids = [t for t in topic_id_query]
    query = Question.objects.all()
    topic_question = {question.topic: question.question for question in query}
    for topic, question in topic_question.items():
        words_scrubbed = [parsing.scrub_name(word)
                          for word in question.split(' ')]
        words = [word for word in words_scrubbed if word]
        if string in words:
            if topic not in topics_ids:
                topics_ids.append(topic)
    topics_return = topics_by_name(topics_ids)
    return topics_return


# Function that returns a random question for a topic.
def random_question(topic):
    topic_id = Topic.objects.filter(name=topic)[0].id
    query = Question.objects.filter(topic=topic_id)
    random_number = random.randrange(
        0, query.count())
    random_question = query[random_number].question
    return random_question


# Given the color of the rating for the topic studied, creates
# a rating instance in the db.
def update_stats(topic_name, color, user):
    topic = Topic.objects.get(name=topic_name)
    rating = Rating()
    rating.rating = color
    rating.topic = topic
    rating.user = user
    rating.save()
    


# TODO: Creates the dict to set the data in the view.
def create_table(user):
    ratings_user = Rating.objects.all().filter(user=user)
    topics = []
    [topics.append(rating.topic) for rating in ratings_user
     if rating.topic not in topics]
    table = {}
    for rating in ratings_user:
        rating_id = rating.id
        info = {rating.created: rating.rating}
        table[rating_id] = info
    pp(table)
        

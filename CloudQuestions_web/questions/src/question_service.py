from questions.models import Topic, Question, Rating
import questions.src.parsing as parsing
import random


# Inserting the questions and answers in the db.
def include_questions(q_a, topic_name):    # pragma: no cover
    topics = list(Topic.query.all())
    if topic_name not in topics:
        topic = Topic()
        topic.name = topic_name
        db.add(topic)
    else:
        topic = Topic.query.get(name=topic_name)
    for q, a in q_a.items():
        if not same_questions(q, topic_name):
            question = Question()
            question.topic = topic.id
            question.question = q
            question.answer = a
            db.add(question)
    db.flush()


# Query of questions given a topic
def questions_by_topic(topic):
    topic_ids = topics_by_id(topic)
    questions = Question.query.filter(topic__in=topic_ids)
    questions = {question.question: question.answer
                 for question in questions}
    db.flush()
    return questions


# Returns a boolean indicating whether the same question already exists
# in the db for a given topic.
def same_questions(question, topic):
    topic = Topic.query.get(name=topic)
    if topic:
        topic_id = topic.id
        query = Question.query.filter(question=question).filter(topic=topic_id)
        db.flush()
        if not query:
            return False
        else:
            return True
    else:
        db.flush()
        return False


# Function that given a list of ids searches for the corresponding
# names in the db.
def topics_by_name(ids):
    query = Topic.query.filter(id__in=ids)
    topic_names = [topic.name for topic in query]
    db.flush()
    return topic_names


# Function that given a name searches for the corresponding
# ids in the db.
def topics_by_id(name):
    query = Topic.query.filter(name__contains=name)
    topic_ids = [topic.id for topic in query]
    db.flush()
    return topic_ids


# Checks if string is any of the topics first. Returns the topics
# where we have any question that contains the string given by the user.
def search_engine(string):
    topics_ids = []
    topic_id_query = topics_by_id(string)
    if topic_id_query:
        topics_ids = [t for t in topic_id_query]
    query = Question.query.all()
    topic_question = {question.topic: question.question for question in query}
    for topic, question in topic_question.items():
        words_scrubbed = [parsing.scrub_name(word)
                          for word in question.split(' ')]
        words = [word for word in words_scrubbed if word]
        if string in words:
            if topic not in topics_ids:
                topics_ids.append(topic)
    topics_return = topics_by_name(topics_ids)
    db.flush()
    return topics_return


# Function that returns a random question for a topic.
def random_question(topic):
    topic_id = Topic.query.filter(name=topic)[0].id
    query = Question.query.filter(topic=topic_id)
    random_number = random.randrange(
        0, query.count())
    random_question = query[random_number].question
    db.flush()
    return random_question


# TODO: Given the color of the rating for the topic studied, creates
# a rating instance in the db.
def update_stats(color):
    pass


# Creates the dict to set the data in the view.
def create_table(user_id):
    ratings = Rating.query.filter(user=user_id)


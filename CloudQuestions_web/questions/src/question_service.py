from db_folder import session_factory
from models.topic import Topic
from models.question import Question
import questions.src.parsing as parsing
import random


# Inserting the questions and answers in the db.
def include_questions(q_a, topic_name):    # pragma: no cover
    session = session_factory.create_session()
    topics = list(session.query(Topic))
    if topic_name not in topics:
        topic = Topic()
        topic.name = topic_name
        session.add(topic)
        session.flush()
    else:
        topic = list(session.query(Topic).filter(Topic.name == topic_name))[0]
    for q, a in q_a.items():
        if not same_questions(q, topic_name):
            question = Question()
            question.topic = topic.id
            question.question = q
            question.answer = a
            session.add(question)
    session.commit()
    session.close()


# Query of questions given a topic
def questions_by_topic(topic):
    session = session_factory.create_session()
    topic_ids = topics_by_id([topic])
    questions = session.query(Question).filter(Question.topic.in_(topic_ids))
    questions = {question.question: question.answer
                 for question in list(questions)}
    session.close()
    return questions


# Returns a boolean indicating whether the same question already exists
# in the db for a given topic.
def same_questions(question, topic):
    session = session_factory.create_session()
    topic = list(session.query(Topic).filter(Topic.name == topic))
    if topic:
        topic_id = topic[0].id
        session = session_factory.create_session()
        query = session.query(Question).filter(Question.question == question
                                               and Question.topic == topic_id)
        session.close()
        if not list(query):
            return False
        else:
            return True
    else:
        session.close()
        return False


# Function that given a list of ids searches for the corresponding
# names in the db.
def topics_by_name(ids):
    session = session_factory.create_session()
    query = list(session.query(Topic.name).filter(Topic.id.in_(ids)))
    topic_names = [topic.name for topic in list(query)]
    session.close()
    return topic_names


# Function that given a list of names searches for the corresponding
# ids in the db.
def topics_by_id(names):
    session = session_factory.create_session()
    pdb.set_trace()
    query = list(session.query(Topic.id).filter(Topic.name.in_(names)))
    topic_ids = [topic.id for topic in list(query)]
    session.close()
    return topic_ids


# Checks if string is any of the topics first. Returns the topics
# where we have any question that contains the string given by the user.
def search_engine(string):
    topics_ids = []
    session = session_factory.create_session()
    topic_id = topics_by_id(string)
    if topic_id:
        topics_ids.append(topic_id)
    topic_question = list(session.query(Question.topic, Question.question))
    for q_elem in topic_question:
        question = q_elem.question
        topic = q_elem.topic
        words_scrubbed = [parsing.scrub_name(word)
                          for word in question.split(' ')]
        words = [word for word in words_scrubbed if word]
        if string in words:
            if topic not in topics_ids:
                topics_ids.append(topic)
    session.close()
    topics_return = topics_by_name(topics_ids)
    return topics_return


# Function that returns a random question for a topic.
def random_question(topic):
    session = session_factory.create_session()
    topic_id = topics_by_id([topic])[0]
    random_number = random.randrange(
        0, session.query(Question).filter(Question.topic == topic_id).count())
    random_question = session.query(
        Question.question).filter(Question.topic == topic_id)[random_number]
    return random_question

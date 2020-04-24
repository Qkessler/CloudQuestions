from data import session_factory
from models.topic import Topic


def questions_by_topic(_topic):
    session = session_factory.create_session()
    query = session.query(Topic).filter(Topic.topic == _topic)
    questions = {topic.question: topic.answer for topic in list(query)}
    session.close()
    return questions


def same_questions(_question):
    session = session_factory.create_session()
    query = session.query(Topic).filter(Topic.question == _question)
    if not list(query):
        return False
    else:
        return True

from data import session_factory
from models.topic import Topic


# Query of questions given a topic
def questions_by_topic(topic):
    session = session_factory.create_session()
    query = session.query(Topic).filter(Topic.topic == topic)
    questions = {topic.question: topic.answer for topic in list(query)}
    session.close()
    return questions


# Returns a boolean indicating whether the same question already exists
# in the db for a given topic.
def same_questions(question, topic):
    session = session_factory.create_session()
    query = session.query(Topic).filter(Topic.question == question
                                        and Topic.topic == topic)
    if not list(query):
        return False
    else:
        return True

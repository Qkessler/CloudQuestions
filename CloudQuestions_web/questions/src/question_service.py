from db_folder import session_factory
from models.topic import Topic
import questions.src.parsing as parsing
import pdb


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
    session.close()
    if not list(query):
        return False
    else:
        return True


# Checks if string is any of the topics first. Returns the topics
# where we have any question that contains the string given by the user.
def search_engine(string):
    topics_return = []
    session = session_factory.create_session()
    topics_query = list(session.query(Topic.topic).distinct())
    topics = [parsing.unscrub_name(topic[0]) for topic in topics_query]
    for t in topics:
        if string.lower() in t.lower():
            topics_return.append(t)
    topic_question = list(session.query(Topic.topic, Topic.question))
    for t_q in topic_question:
        question = t_q[1]
        topic = t_q[0]
        words_scrubbed = [parsing.scrub_name(word)
                          for word in question.split(' ')]
        words = [word for word in words_scrubbed if word]
        if string in words:
            if topic not in topics_return:
                topics_return.append(parsing.unscrub_name(topic))
    session.close()
    return topics_return

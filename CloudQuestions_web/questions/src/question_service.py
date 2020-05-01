from db_folder import session_factory
from models.topic import Topic
from models.question import Question
import questions.src.parsing as parsing
import pdb


# Inserting the questions and answers in the db.
def include_questions(q_a, topic_name):    # pragma: no cover
    session = session_factory.create_session()
    pdb.set_trace()
    topics = list(session.query(Topic))
    if topic_name not in topics:
        topic = Topic()
        topic.name = topic_name
        session.add(topic)
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
    questions = session.query(Question).filter(Question.topic == topic)
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


# Checks if string is any of the topics first. Returns the topics
# where we have any question that contains the string given by the user.
def search_engine(string):
    topics_return = []
    session = session_factory.create_session()
    topics_query = list(session.query(Topic.name))
    topics = [parsing.unscrub_name(topic[0]) for topic in topics_query]
    for t in topics:
        if string.lower() in t.lower():
            topics_return.append(t)
    topic_question = list(session.query(Question.topic, Question.question))
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
